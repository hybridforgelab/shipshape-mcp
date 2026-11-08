"""hybridforgelab-shipshape-mcp moved to bytestay-shipshape-mcp. This package only forwards to it."""
import sys

__version__ = "0.3.0"

NOTICE = ("hybridforgelab-shipshape-mcp has moved to bytestay-shipshape-mcp. This name only forwards to it and gets no more updates. "
          "Switch your MCP config to: uvx --from bytestay-shipshape-mcp shipshape-mcp")


def main() -> None:
    """Print the notice on stderr (stdout is the MCP stdio channel), then run the ByteStay server."""
    print(NOTICE, file=sys.stderr, flush=True)
    from shipshape_mcp.server import main as bytestay_main

    bytestay_main()
