from fastmcp import Client

from app.core.config import config as c

mcp_client = Client(transport=f"{c.MCP_REMOTE_HOST_URL}:{c.MCP_REMOTE_HOST_PORT}/mcp")
