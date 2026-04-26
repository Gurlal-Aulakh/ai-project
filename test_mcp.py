import asyncio
from app.mcp_client import get_project_overview_from_mcp, get_project_stack_from_mcp


async def main():
    print("Testing MCP overview...")
    overview = await get_project_overview_from_mcp()
    print(overview)

    print("\nTesting MCP stack...")
    stack = await get_project_stack_from_mcp()
    print(stack)


if __name__ == "__main__":
    asyncio.run(main())