"""MCP resource server."""
import asyncio

from fastmcp import FastMCP

from app.repository.storage import _gcs

mcp = FastMCP(name="ResourceServer")


@mcp.resource(
    uri="resource://planner/{input_name}",
    name="planner_input_resource",
    description="Get input placeholder for Planner Agent prompt.",
    tags={"planner", "resource"},
    enabled=True,
)
async def get_planner_input(input_name: str) -> str:
    """Get input for Planner agent prompt from GCS.

    Args:
        input_name (str): input name.

    Returns:
        str: input content.
    """
    blob_name = input_name + ".json"
    content = await asyncio.to_thread(_gcs.get, blob_name)
    return content


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
