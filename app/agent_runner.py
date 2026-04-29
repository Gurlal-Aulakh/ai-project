import os
import asyncio
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, set_default_openai_client

from app.config import get_settings
from app.prompts import load_prompt
from app.retrieval import setup_collection
# from app.graph_seed import seed_project_graph
from app.cache import get_cached_value, set_cached_value
from app.hybrid_retrieval import hybrid_search
from app.semantic_cache import check_semantic_cache, save_semantic_cache
from app.cache_policy import should_cache_response, build_cache_metadata

from app.workers import run_concept_agent, run_project_agent
from app.mcp_client import get_project_overview_from_mcp, get_project_stack_from_mcp
from app.memory import store_memory, get_memory
# from app.graph_db import get_project_relationships, get_entity_relationships

os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "0"

settings = get_settings()
client = AsyncOpenAI(api_key=settings.openai_api_key)
set_default_openai_client(client)


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
async def ask_concept_agent(question: str) -> str:
    print("TOOL USED: ask_concept_agent")
    return await run_concept_agent(question)


@function_tool
async def ask_project_agent(question: str) -> str:
    print("TOOL USED: ask_project_agent")
    context = hybrid_search(question)

    return await run_project_agent(
        f"""
Use this project context:
{context}

Now answer:
{question}
"""
    )


@function_tool
async def mcp_project_overview() -> str:
    print("TOOL USED: mcp_project_overview")
    return await get_project_overview_from_mcp()


@function_tool
async def mcp_project_stack() -> str:
    print("TOOL USED: mcp_project_stack")
    return await get_project_stack_from_mcp()


@function_tool
def save_user_preference(key: str, value: str) -> str:
    print("TOOL USED: save_user_preference")
    store_memory(key, value)
    return "Saved successfully."


@function_tool
def load_user_memory() -> str:
    print("TOOL USED: load_user_memory")
    return str(get_memory())


# @function_tool
# def query_project_graph() -> str:
#     print("TOOL USED: query_project_graph")
#     return get_project_relationships()


# @function_tool
# def query_entity_graph(entity_name: str) -> str:
#     print("TOOL USED: query_entity_graph")
#     return get_entity_relationships(entity_name)


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
            # query_project_graph,
            # query_entity_graph,
        ],
        model="gpt-4.1",
    )


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


async def run_ai_assistant(user_input: str) -> dict:
    setup_collection()
    # seed_project_graph()

    cached_answer = check_semantic_cache(user_input)

    if cached_answer:
        return {
            "answer": cached_answer,
            "cache_status": "HIT",
            "tools_used": [],
            "debug": "Returned from semantic cache.",
        }

    agent = build_agent()

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
   - Relationship question → graph tools
5. Final answer must be grounded in retrieved context.

Answer clearly for a beginner.
"""
    )

    tools_used = extract_tools_used(result)
    metadata = build_cache_metadata(user_input, tools_used)

    cache_status = "MISS"

    if should_cache_response(tools_used):
        save_semantic_cache(user_input, result.final_output, metadata=metadata)
        cache_status = "MISS → SAVED"
    else:
        cache_status = "MISS → NOT SAVED"

    return {
        "answer": result.final_output,
        "cache_status": cache_status,
        "tools_used": tools_used,
        "debug": str(result),
    }


def run_ai_assistant_sync(user_input: str) -> dict:
    return asyncio.run(run_ai_assistant(user_input))