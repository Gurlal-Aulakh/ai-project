from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def call_mcp_tool(tool_name: str) -> str:
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments={},
            )

            if result.content:
                return result.content[0].text

            return "MCP tool returned no content."


async def get_project_overview_from_mcp() -> str:
    return await call_mcp_tool("get_project_overview")


async def get_project_stack_from_mcp() -> str:
    return await call_mcp_tool("get_project_stack")