# hybridforgelab-shipshape-mcp: moved to bytestay-shipshape-mcp

This package has moved to **[bytestay-shipshape-mcp](https://pypi.org/project/bytestay-shipshape-mcp/)**. Hybrid Forge Lab is now ByteStay.

This last version only installs bytestay-shipshape-mcp and forwards to it. It prints a one-line notice on stderr and gets no more updates.

## Switch

Replace `hybridforgelab-shipshape-mcp` with `bytestay-shipshape-mcp` in your MCP client config:

```json
"command": "uvx",
"args": ["--from", "bytestay-shipshape-mcp", "shipshape-mcp"]
```

Or with Claude Code:

```bash
claude mcp add shipshape --env RAPIDAPI_KEY=your-rapidapi-key -- uvx --from bytestay-shipshape-mcp shipshape-mcp
```

The environment variables are the same, so your keys keep working.

## Links

- Package: [bytestay-shipshape-mcp](https://pypi.org/project/bytestay-shipshape-mcp/)
- Source: [Bytestay/shipshape-mcp](https://github.com/Bytestay/shipshape-mcp)
- Shipshape API: [shipshape.bytestay.pt](https://shipshape.bytestay.pt)
