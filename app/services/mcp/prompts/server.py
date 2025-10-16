"""MCP prompt server."""
from fastmcp import FastMCP

from app.repository.prompt import (
    get_extraction_prompt, get_text_to_sql_prompt, get_pfa_planner_prompt
)

mcp = FastMCP(name="PromptServer")
mcp.prompt(
    get_extraction_prompt,
    name="extraction",
    tags={"extraction"},
    enabled=True,
)
mcp.prompt(
    get_text_to_sql_prompt,
    name="text-to-sql",
    tags={"text-to-sql"},
    enabled=True,
)
mcp.prompt(
    get_pfa_planner_prompt,
    name="pfa-planner",
    tags={"planner", "pfa"},
    enabled=True,
)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
