from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


class MCPError(Exception):
    pass


@dataclass(frozen=True)
class Capability:
    name: str
    kind: str
    description: str
    input_schema: dict[str, Any] | None = None
    risk: str = "low"
    tenant: str | None = None


@dataclass(frozen=True)
class ToolCall:
    call_id: str
    tool: str
    arguments: dict[str, Any]
    tenant_id: str


@dataclass(frozen=True)
class ToolResult:
    call_id: str
    ok: bool
    output: Any
    trusted: bool = False


class MCPServer:
    """Small in-memory educational server, not a wire-protocol implementation."""

    def __init__(self, capabilities: list[Capability], handlers: dict[str, Callable[..., Any]]):
        self.capabilities = {c.name: c for c in capabilities}
        self.handlers = handlers

    def list_capabilities(self) -> list[Capability]:
        return list(self.capabilities.values())

    def call_tool(self, call: ToolCall) -> ToolResult:
        cap = self.capabilities.get(call.tool)
        if not cap or cap.kind != "tool":
            raise MCPError("unknown or non-tool capability")
        handler = self.handlers.get(call.tool)
        if not handler:
            raise MCPError("tool has no implementation")
        try:
            output = handler(**call.arguments)
            return ToolResult(call.call_id, True, output, trusted=False)
        except TypeError as exc:
            raise MCPError(f"invalid tool arguments: {exc}") from exc


class MCPClient:
    def __init__(self, tenant_id: str, allowed_tools: set[str]):
        self.tenant_id = tenant_id
        self.allowed_tools = allowed_tools
        self.capabilities: dict[str, Capability] = {}

    def discover(self, server: MCPServer) -> list[Capability]:
        discovered = server.list_capabilities()
        self.capabilities = {c.name: c for c in discovered if c.kind in {"tool", "resource", "prompt"}}
        return list(self.capabilities.values())

    def allowed(self, tool: str) -> bool:
        return tool in self.allowed_tools and tool in self.capabilities and self.capabilities[tool].kind == "tool"

    def call(self, server: MCPServer, call: ToolCall) -> ToolResult:
        if call.tenant_id != self.tenant_id:
            raise MCPError("tenant mismatch")
        if not self.allowed(call.tool):
            raise MCPError("capability denied by client policy")
        return server.call_tool(call)


def redact(value: Any, secrets: list[str]) -> Any:
    if isinstance(value, str):
        for secret in secrets:
            value = value.replace(secret, "[REDACTED]")
        return value
    if isinstance(value, dict):
        return {k: redact(v, secrets) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v, secrets) for v in value]
    return value
