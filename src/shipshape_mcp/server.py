"""Shipshape MCP server: lint Dockerfiles and Kubernetes manifests (Pod Security Standards, A–F grade)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Literal

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import Field

from . import files
from .client import PRODUCTS, call

PRODUCT = PRODUCTS["shipshape"]
MAX_FILE = 512 * 1024
Severity = Literal["high", "medium", "low", "info", "never"]

server = MCPServer(
    "shipshape",
    title="Shipshape: Dockerfile and Kubernetes lint",
    instructions=(
        "Lint a Dockerfile or Kubernetes manifest before you hand it over: root in the final stage, unpinned base "
        "images, curl | sh, secrets in ENV/ARG, Pod Security Standards, resources and probes. Every finding has the "
        "line, a fix and the standard behind it, and the file gets an A–F grade. Content is processed in memory and "
        "not stored. Each call is one request on the user's Shipshape plan."
    ),
    website_url="https://shipshape.hybridforgelab.com",
)


def _type_for(path: str) -> str:
    name = Path(path).name.lower()
    if name in ("dockerfile", "containerfile") or name.endswith(".dockerfile") or name.startswith("dockerfile."):
        return "dockerfile"
    return "auto"


@server.tool(annotations=ToolAnnotations(read_only_hint=True, open_world_hint=True))
async def lint(
    content: Annotated[str | dict | list | None,
                       Field(description="The Dockerfile or manifest, as text (up to 512 KiB).")] = None,
    path: Annotated[str | None, Field(description="A local file to lint instead of `content`.")] = None,
    type: Annotated[Literal["auto", "dockerfile", "kubernetes"],
                    Field(description="auto detects Dockerfile vs Kubernetes YAML/JSON.")] = "auto",
    fail_on: Annotated[Severity, Field(description="`passed` is false at this severity or worse.")] = "high",
    ignore: Annotated[list[str] | None, Field(description='Rule ids to skip, e.g. ["DF-017"].')] = None,
) -> dict:
    """Lint a Dockerfile or Kubernetes manifest. Returns the grade, score, `passed` and every finding with its
    line, fix and reference. Give either `content` or `path`."""
    if bool(content) == bool(path):
        raise ToolError("Give exactly one of content or path.")
    if path:
        content = files.read_text(path, MAX_FILE)
        if type == "auto":
            type = _type_for(path)
    elif not isinstance(content, str):
        # A JSON manifest the client (or the SDK) sent as an object: back to text for the linter.
        content = json.dumps(content, indent=2)
    body = {"content": content, "type": type, "fail_on": fail_on}
    if ignore:
        body["ignore"] = ignore
    return await call(PRODUCT, "POST", "/v1/lint", json=body)


def main() -> None:  # pragma: no cover - stdio entry point
    server.run("stdio")

if __name__ == "__main__":  # pragma: no cover
    main()
