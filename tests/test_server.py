import json

import pytest
from mcp.server.mcpserver.exceptions import ToolError

from shipshape_mcp import files
from shipshape_mcp import server as shipshape

SPEC_V1 = "openapi: 3.0.3\ninfo: {title: t, version: '1'}\npaths: {}\n"
SPEC_V2 = "openapi: 3.0.3\ninfo: {title: t, version: '2'}\npaths: {}\n"


async def test_server_lists_its_tools():
    listed = await shipshape.server.list_tools()
    assert {t.name for t in listed} == {"lint"}
    for t in listed:
        assert t.description and t.annotations.read_only_hint is True and t.annotations.open_world_hint is True


async def test_shipshape_content_and_path(api, tmp_path):
    await shipshape.lint(content="FROM node", fail_on="medium", ignore=["DF-017"])
    assert api.last.url.path == "/v1/lint"
    assert api.last_json() == {"content": "FROM node", "type": "auto", "fail_on": "medium", "ignore": ["DF-017"]}
    for name, expected in (("Dockerfile", "dockerfile"), ("api.Dockerfile", "dockerfile"),
                           ("Dockerfile.prod", "dockerfile"), ("Containerfile", "dockerfile"), ("deploy.yaml", "auto")):
        f = tmp_path / name
        f.write_text("FROM node\n")
        await shipshape.lint(path=str(f))
        assert api.last_json()["type"] == expected and api.last_json()["content"] == "FROM node\n"
        assert "ignore" not in api.last_json()
    await shipshape.lint(path=str(tmp_path / "deploy.yaml"), type="kubernetes")
    assert api.last_json()["type"] == "kubernetes"
    with pytest.raises(ToolError, match="exactly one"):
        await shipshape.lint()


async def test_text_file_errors(tmp_path):
    binary = tmp_path / "Dockerfile"
    binary.write_bytes(b"\xff\xfe\x00")
    with pytest.raises(ToolError, match="not UTF-8"):
        files.read_text(str(binary), 100)
    with pytest.raises(ToolError, match="limit is"):
        files.read_text(str(binary), 1)


async def test_json_manifest_through_the_server(api):
    await shipshape.server.call_tool("lint", {"content": '{"apiVersion": "v1", "kind": "Pod"}'})
    assert json.loads(api.last_json()["content"]) == {"apiVersion": "v1", "kind": "Pod"}


async def test_text_file_limits(tmp_path):
    with pytest.raises(ToolError, match="No such file"):
        files.read_text(str(tmp_path / "missing"), 100)
    big = tmp_path / "big"
    big.write_text("x" * 50)
    with pytest.raises(ToolError, match="limit is"):
        files.read_text(str(big), 10)
    binary = tmp_path / "bin"
    binary.write_bytes(b"\xff\xfe\x00")
    with pytest.raises(ToolError, match="not UTF-8"):
        files.read_text(str(binary), 100)
