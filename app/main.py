import asyncio
import os

os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "0"

from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, set_default_openai_client
from app.workers import run_concept_agent, run_project_agent
from app.config import get_settings
from app.prompts import load_prompt
from app.retrieval import setup_collection, seed_documents, search_documents
from app.cache import get_cached_value, set_cached_value
from app.memory import store_memory, get_memory
from app.semantic_cache import check_semantic_cache, save_semantic_cache
from app.mcp_client import get_project_overview_from_mcp, get_project_stack_from_mcp
from app.graph_seed import seed_project_graph
from app.graph_db import get_project_relationships, get_entity_relationships
from app.cache_policy import should_cache_response, build_cache_metadata
from app.hybrid_retrieval import hybrid_search

settings = get_settings()

# Set OpenAI client for Agents SDK
client = AsyncOpenAI(api_key=settings.openai_api_key)
set_default_openai_client(client)

@function_tool
def query_project_graph() -> str:
    print("TOOL USED: query_project_graph")
    return get_project_relationships()


@function_tool
def query_entity_graph(entity_name: str) -> str:
    print("TOOL USED: query_entity_graph")
    return get_entity_relationships(entity_name)

@function_tool
def save_user_preference(key: str, value: str) -> str:
    print("TOOL USED: save_user_preference")
    store_memory(key, value)
    return "Saved successfully."


@function_tool
def load_user_memory() -> str:
    print("TOOL USED: load_user_memory")
    memory = get_memory()
    return str(memory)


@function_tool
def retrieve_context(query: str) -> str:
    print("TOOL USED: retrieve_context")

    cache_key = f"retrieval:{query}"
    cached = get_cached_value(cache_key)
    if cached:
        return f"[CACHE HIT]\n{cached}"

    result = hybrid_search(query)
    set_cached_value(cache_key, result, ttl_seconds=3600)
    return result

@function_tool
async def mcp_project_overview() -> str:
    print("TOOL USED: mcp_project_overview")
    return await get_project_overview_from_mcp()


@function_tool
async def mcp_project_stack() -> str:
    print("TOOL USED: mcp_project_stack")
    return await get_project_stack_from_mcp()

@function_tool
async def ask_concept_agent(question: str) -> str:
    print("TOOL USED: ask_concept_agent")
    return await run_concept_agent(question)


# @function_tool
# async def ask_project_agent(question: str) -> str:
#     print("TOOL USED: ask_project_agent")
#     return await run_project_agent(question)

@function_tool
async def ask_project_agent(question: str) -> str:
    
    # ❌ DO NOT call retrieve_context directly
    print("TOOL USED: ask_project_agent")
    context = search_documents(question)   # ✅ use raw function

    return await run_project_agent(
        f"""
Use this context:
{context}

Answer:
{question}
"""
    )

# @function_tool
# def mcp_project_info() -> str:
#     return asyncio.run(call_project_info_tool())


def build_agent() -> Agent:
    instructions = load_prompt("main_agent.v1.txt")
    return Agent(
        name="MainAgent",
        instructions=instructions,
        tools=[
    retrieve_context,
    ask_concept_agent,
    ask_project_agent,
    mcp_project_overview,
    mcp_project_stack,
    save_user_preference,
    load_user_memory,
    query_project_graph,
    query_entity_graph,
],
        model="gpt-4.1",
    )


async def run_app() -> None:
    print("STEP 1: Setting up collection")
    setup_collection()

    print("STEP 2: Seeding documents")
    seed_documents()

    print("STEP 2.5: Seeding graph database")
    seed_project_graph()

    print("STEP 3: Building agent")
    agent = build_agent()

    print("STEP 4: Waiting for input...")
    user_input = input("Ask Something: ")
    
    print("STEP 4.5: Checking semantic cache")
    cached_answer = check_semantic_cache(user_input)

    if cached_answer:
        print("SEMANTIC CACHE HIT")
        print("\n--- RESPONSE FROM SEMANTIC CACHE ---")
        print(cached_answer)
        return

    print("SEMANTIC CACHE MISS")

    print("STEP 5: Running agent...")

    result = await Runner.run(
        agent,
        input=f"""
User question: {user_input}

Steps you MUST follow:

1. Load user memory.
2. Retrieve relevant context using retrieve_context.
3. Use BOTH memory and retrieved context in your reasoning.
4. Then decide:
   - Concept question → ask_concept_agent
   - Project question → ask_project_agent
   - Tool question → MCP
5. Final answer must be grounded in retrieved context.

Answer clearly for a beginner.
""")
    
    # print("\n--- DEBUG: FULL RESULT ---")
    # print(result)
    # print("\n ----------------------------------------------------------------------------------\n")
    # print("\n--- DEBUG: TOOL CALLS ---")
    # for item in result.new_items:
    #     print(item)


    def extract_tools_used(result) -> list[str]:
        tools = []

        for item in result.new_items:
            raw_item = getattr(item, "raw_item", None)

            if raw_item is None:
                continue

            name = getattr(raw_item, "name", None)

            if name:
                tools.append(name)

        return tools

    tools_used = extract_tools_used(result)
    print("TOOLS USED:", tools_used)

    tools_used = extract_tools_used(result)
    metadata = build_cache_metadata(user_input, tools_used)

    if should_cache_response(tools_used):
        save_semantic_cache(user_input, result.final_output, metadata=metadata)
        print("SAVED TO SEMANTIC CACHE")
    else:
        print("NOT SAVED TO SEMANTIC CACHE")

    print("STEP 6: Done")
    print("\n--- RESPONSE ---")
    print(result.final_output)
    save_semantic_cache(user_input, result.final_output)
    print("SAVED TO SEMANTIC CACHE")


if __name__ == "__main__":
    asyncio.run(run_app())
