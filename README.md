# Shipshape MCP server

Let your coding agent lint a Dockerfile or Kubernetes manifest before handing it over: root in the final stage, unpinned base images, `curl | sh`, secrets in ENV/ARG, Pod Security Standards, resources and probes.

The server is open source (MIT). It calls the [Shipshape API](https://shipshape.hybridforgelab.com), which is paid, with a free plan.

- You use **your own key, from RapidAPI or api.market**.
- Every tool call is one request on your plan.
- The free Basic plan has 15 requests a month, with a hard limit, so it never runs up a bill.

## 1. Get a key

| marketplace | |
|---|---|
| RapidAPI | [plans](https://rapidapi.com/hybrid-forge-lab-hybrid-forge-lab-default/api/shipshape-dockerfile-and-kubernetes-lint-api/pricing) |
| api.market | [store](https://api.market/store/hybrid-forge-lab/shipshape) |

## 2. Add the server to your MCP client

The server runs locally over stdio with [uv](https://docs.astral.sh/uv/). Put your key in its environment.

**JSON configuration** (Claude Desktop, Cursor, VS Code and most clients):

```json
{
  "mcpServers": {
    "shipshape": {
      "command": "uvx",
      "args": ["--from", "hybridforgelab-shipshape-mcp", "shipshape-mcp"],
      "env": { "RAPIDAPI_KEY": "your-rapidapi-key" }
    }
  }
}
```

**Claude Code:**

```bash
claude mcp add shipshape --env RAPIDAPI_KEY=your-rapidapi-key -- uvx --from hybridforgelab-shipshape-mcp shipshape-mcp
```

### Environment

| variable | meaning |
|---|---|
| `RAPIDAPI_KEY` | your RapidAPI key |
| `API_MARKET_KEY` | your api.market key, used when `RAPIDAPI_KEY` is not set |
| `HFL_MARKETPLACE` | `rapidapi` or `apimarket`, when both keys are set |

Without a key the server still starts. The first tool call then explains where to get one.

## 3. Tools

| tool | what it does |
|---|---|
| `lint(content=… \| path=…, type="auto", fail_on="high", ignore=[…])` | lints one file and returns the A–F grade, score, `passed` and every finding with its line, fix and reference |

- With `path`, files named like `Dockerfile`, `*.Dockerfile`, `Dockerfile.*` or `Containerfile` are linted as Dockerfiles.
- `passed` is false when a finding is at or above `fail_on`.

Every tool returns the API's JSON response.

- When the marketplace reports it, `quota_remaining` is added: the requests left on your plan this month.
- Errors are explained in plain words, with what to do next:
  - key refused, with the link to subscribe;
  - quota reached, with the plans;
  - input the API couldn't process, with the API's reason.

## Privacy

- Local files are read only when a tool is given their path. They are sent to the API for that one request.
- The API processes inputs in memory and doesn't store them. See the [privacy policy](https://shipshape.hybridforgelab.com/privacy.html).
- Your key is only sent to the marketplace you chose.

## Limits

- Files up to 512 KiB.
- Helm templates must be rendered first (`helm template`).
- NetworkPolicies, PodDisruptionBudgets and RBAC are not checked.
- The server needs Python 3.10+ (uv installs it for you).

## Development

```bash
uv venv && uv pip install -e ".[dev]"
.venv/bin/pytest            # unit tests, no network; 100% coverage required
.venv/bin/ruff check src tests scripts
```

`scripts/e2e_stdio.py shipshape` runs the server over stdio, as a client would, and calls its tools against the real API. It needs `RAPIDAPI_KEY` or `API_MARKET_KEY`.

## Licence

MIT. Shipshape itself is a paid API with a free plan, run by [Hybrid Forge Lab](https://hybridforgelab.com).
