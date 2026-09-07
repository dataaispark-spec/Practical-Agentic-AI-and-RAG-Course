from app.mcp_client import Capability, MCPClient, MCPError, MCPServer, ToolCall, redact


def server():
    return MCPServer(
        [
            Capability("calculator", "tool", "safe calculation"),
            Capability("admin_delete", "tool", "dangerous", risk="high"),
            Capability("docs", "resource", "documentation"),
        ],
        {"calculator": lambda x: x * 2, "admin_delete": lambda x: f"deleted:{x}"},
    )


def test_discovery_filters_to_known_capability_kinds():
    c=MCPClient("t1", {"calculator"})
    caps=c.discover(server())
    assert {x.name for x in caps}=={"calculator","admin_delete","docs"}


def test_allowed_call():
    c=MCPClient("t1", {"calculator"}); s=server(); c.discover(s)
    result=c.call(s, ToolCall("1","calculator",{"x":3},"t1"))
    assert result.output==6 and not result.trusted


def test_unauthorized_tool_denied():
    c=MCPClient("t1", {"calculator"}); s=server(); c.discover(s)
    try: c.call(s, ToolCall("1","admin_delete",{"x":"7"},"t1"))
    except MCPError as e: assert "denied" in str(e)
    else: raise AssertionError("expected denial")


def test_tenant_isolation():
    c=MCPClient("t1", {"calculator"}); s=server(); c.discover(s)
    try: c.call(s, ToolCall("1","calculator",{"x":3},"t2"))
    except MCPError as e: assert "tenant" in str(e)
    else: raise AssertionError("expected tenant denial")


def test_redaction():
    assert redact({"token":"abc","nested":["abc",1]}, ["abc"])=={"token":"[REDACTED]","nested":["[REDACTED]",1]}
