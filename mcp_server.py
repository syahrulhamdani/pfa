from importlib import import_module
from typing import Annotated

from typer import Typer, Argument

app = Typer(name="MCP runner")


@app.command()
def run_mcp_server(
    name: Annotated[str, Argument(help="MCP server name")],
    transport: Annotated[str, Argument(help="MCP transport")] = "streamable-http",
    port: Annotated[int, Argument(help="MCP port")] = 7001,
):
    """Run MCP server."""
    module = import_module(f"app.services.mcp.{name}.server")

    if not hasattr(module, "mcp"):
        raise AttributeError("MCP server not found")

    module.mcp.run(transport=transport, port=port)


if __name__ == "__main__":
    app()
