"""MCP resources."""
import asyncio

from app.core.config import config as c
from app.repository.storage import Storage

_gcs = Storage(bucket_id=c.GCS_BUCKET_ID)


async def get_planner_input(input_name: str) -> str:
    """Get input for Planner agent prompt from GCS.

    This coroutine is used as MCP resource template for planner prompt input.

    Args:
        input_name (str): input name.

    Returns:
        str: input content.
    """
    content = await asyncio.to_thread(_gcs.get, input_name, "mcp/resource", "json")
    return content
