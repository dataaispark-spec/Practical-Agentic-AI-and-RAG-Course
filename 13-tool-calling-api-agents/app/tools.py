from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

class Risk(str, Enum):
    READ = "read"
    WRITE = "write"
    HIGH_IMPACT = "high_impact"

@dataclass(frozen=True)
class Tool:
    name: str
    handler: Callable[..., Any]
    required_role: str
    risk: Risk
    idempotent: bool = True

class ToolError(Exception): pass
class PolicyDenied(ToolError): pass
class ApprovalRequired(ToolError): pass

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}
        self._completed: dict[str, Any] = {}

    def register(self, tool: Tool):
        if tool.name in self._tools:
            raise ValueError(f"duplicate tool: {tool.name}")
        self._tools[tool.name] = tool

    def call(self, name: str, *, role: str, idempotency_key: str | None = None,
             approved: bool = False, args: dict[str, Any] | None = None):
        if name not in self._tools:
            raise ToolError("UNKNOWN_TOOL")
        tool = self._tools[name]
        if role != tool.required_role:
            raise PolicyDenied("POLICY_DENIED")
        if tool.risk is Risk.HIGH_IMPACT and not approved:
            raise ApprovalRequired("APPROVAL_REQUIRED")
        if tool.idempotent and idempotency_key and idempotency_key in self._completed:
            return self._completed[idempotency_key]
        try:
            result = tool.handler(**(args or {}))
        except TypeError as exc:
            raise ToolError("VALIDATION_ERROR") from exc
        if tool.idempotent and idempotency_key:
            self._completed[idempotency_key] = result
        return result
