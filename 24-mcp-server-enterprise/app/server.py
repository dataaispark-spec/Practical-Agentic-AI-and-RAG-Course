from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Callable


class ServerError(Exception):
    pass


@dataclass(frozen=True)
class Principal:
    subject: str
    tenant_id: str
    roles: frozenset[str]


@dataclass(frozen=True)
class Capability:
    name: str
    kind: str
    version: str = "1"
    risk: str = "low"
    roles: frozenset[str] = frozenset()


@dataclass(frozen=True)
class Request:
    request_id: str
    capability: str
    arguments: dict[str, Any]
    tenant_id: str
    idempotency_key: str | None = None


def canonical_hash(request: Request) -> str:
    payload = {
        "capability": request.capability,
        "arguments": request.arguments,
        "tenant_id": request.tenant_id,
    }
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class EnterpriseServer:
    def __init__(self, capabilities: list[Capability], handlers: dict[str, Callable[..., Any]]):
        self.capabilities = {c.name: c for c in capabilities}
        self.handlers = handlers
        self.effects: dict[str, Any] = {}
        self.audit: list[dict[str, Any]] = []

    def discover(self) -> list[Capability]:
        return list(self.capabilities.values())

    def authorize(self, principal: Principal, request: Request) -> None:
        if principal.tenant_id != request.tenant_id:
            raise ServerError("tenant mismatch")
        cap = self.capabilities.get(request.capability)
        if not cap:
            raise ServerError("unknown capability")
        if cap.roles and not (principal.roles & cap.roles):
            raise ServerError("role denied")

    def execute(self, principal: Principal, request: Request) -> Any:
        self.authorize(principal, request)
        cap = self.capabilities[request.capability]
        action = canonical_hash(request)
        if cap.risk == "high" and request.idempotency_key is None:
            raise ServerError("high-risk mutation requires idempotency key")
        if request.idempotency_key and request.idempotency_key in self.effects:
            return self.effects[request.idempotency_key]
        handler = self.handlers.get(request.capability)
        if not handler:
            raise ServerError("handler unavailable")
        try:
            result = handler(**request.arguments)
        except TypeError as exc:
            raise ServerError(f"invalid arguments: {exc}") from exc
        if request.idempotency_key:
            self.effects[request.idempotency_key] = result
        self.audit.append({
            "request_id": request.request_id,
            "tenant_id": principal.tenant_id,
            "subject": principal.subject,
            "capability": request.capability,
            "action_hash": action,
            "version": cap.version,
        })
        return result
