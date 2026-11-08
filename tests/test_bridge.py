from shipshape_mcp import server

import hybridforgelab_shipshape_mcp as bridge


def test_main_prints_the_notice_on_stderr_and_runs_the_bytestay_server(monkeypatch, capsys):
    calls = []
    monkeypatch.setattr(server, "main", lambda: calls.append("run"))
    bridge.main()
    out, err = capsys.readouterr()
    assert calls == ["run"]
    assert out == ""
    assert "bytestay-shipshape-mcp" in err and "uvx --from bytestay-shipshape-mcp shipshape-mcp" in err
    assert err.count("\n") == 1
