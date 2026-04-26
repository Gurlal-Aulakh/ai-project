from mcp.server.fastmcp import FastMCP

mcp = FastMCP("phase3-project-tools")


@mcp.tool()
def get_project_overview() -> str:
    """
    Returns a short overview of this AI project.
    """
    return (
        "This project is an AI assistant built in phases. "
        "Phase 1 added a main agent, prompt versioning, vector database retrieval, "
        "Redis caching, and basic MCP setup. "
        "Phase 2 added worker agents: a ConceptExplainerAgent and a ProjectGuideAgent. "
        "Phase 3 focuses on proper MCP integration, long-term memory, and better tracing."
    )


@mcp.tool()
def get_project_stack() -> str:
    """
    Returns the technology stack used in this project.
    """
    return (
        "Technology stack: Python, OpenAI Agents SDK, Qdrant vector database, "
        "Redis cache, MCP Python SDK, prompt files, and worker agents."
    )


if __name__ == "__main__":
    mcp.run()