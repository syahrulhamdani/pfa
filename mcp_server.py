from importlib import import_module
from typing import Annotated

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastmcp import FastMCP

from app.core.config import config as c
from app.services.mcp.prompts import (get_extraction_prompt,
                                      get_pfa_planner_prompt,
                                      get_text_to_sql_prompt)
from app.services.mcp.resources import get_planner_input

mcp = FastMCP(name="PersonalFinanceAssistantService", stateless_http=True)

# Prompts
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

# Resources
mcp.resource(
    uri="resource://planner/{input_name}",
    name="planner_input_resource",
    description="Get input placeholder for Planner Agent prompt.",
    tags={"planner", "resource"},
    enabled=True,
)(get_planner_input)

# HTTP server
mcp_app = mcp.streamable_http_app(path=c.MCP_API_PREFIX)
app = FastAPI(
    title="MCP Server for Personal Finance Assistant",
    lifespan=mcp_app.lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return JSONResponse({"status": "healthy", "service": mcp.name})


app.mount("/", mcp_app)
