CACHEABLE_TOOLS = {
    "ask_concept_agent",
    "ask_project_agent",
    "mcp_project_overview",
    "mcp_project_stack",
    "retrieve_context",
    "query_project_graph",
    "query_entity_graph",
    "load_user_memory",
}

NON_CACHEABLE_TOOLS = {
    "save_user_preference",
}


def should_cache_response(tools_used: list[str]) -> bool:
    if not tools_used:
        return True

    if any(tool in NON_CACHEABLE_TOOLS for tool in tools_used):
        return False

    return any(tool in CACHEABLE_TOOLS for tool in tools_used)


def build_cache_metadata(user_input: str, tools_used: list[str]) -> dict:
    return {
        "cache_allowed": should_cache_response(tools_used),
        "tools_used": ",".join(tools_used),
        "user_id": "default",
        "query_type": classify_query_type(user_input),
    }


def classify_query_type(user_input: str) -> str:
    text = user_input.lower()

    if any(word in text for word in ["what is", "explain", "define"]):
        return "concept"

    if any(word in text for word in ["project", "stack", "architecture"]):
        return "project"

    if any(word in text for word in ["connect", "relationship", "related"]):
        return "graph"

    if any(word in text for word in ["remember", "i like", "i love", "i prefer"]):
        return "memory"

    return "general"