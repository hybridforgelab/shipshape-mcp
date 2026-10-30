"""Reading local files for tools that accept a path instead of the content."""
from __future__ import annotations

from pathlib import Path

from mcp.server.mcpserver.exceptions import ToolError


def resolve(path: str) -> Path:
    p = Path(path).expanduser()
    if not p.is_file():
        raise ToolError(f"No such file: {p} (relative paths start from {Path.cwd()}).")
    return p


def read_text(path: str, max_bytes: int) -> str:
    p = resolve(path)
    size = p.stat().st_size
    if size > max_bytes:
        raise ToolError(f"{p} is {size:,} bytes; the limit is {max_bytes:,}.")
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ToolError(f"{p} is not UTF-8 text.")
