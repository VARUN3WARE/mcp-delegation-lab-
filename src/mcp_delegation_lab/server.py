from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .audit import AuditLogger
from .store import MockUnitsStore
from .tools import register_tools


def create_app() -> FastMCP:
    store = MockUnitsStore.seed_default()
    audit = AuditLogger()
    mcp = FastMCP("mcp-delegation-lab")
    register_tools(mcp, store, audit)
    return mcp


def main() -> None:
    app = create_app()
    app.run()


if __name__ == "__main__":
    main()
