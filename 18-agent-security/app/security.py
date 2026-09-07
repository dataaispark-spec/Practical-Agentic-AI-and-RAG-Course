from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import ipaddress
import re
from urllib.parse import urlparse


class Trust(str, Enum):
    TRUSTED_SYSTEM = "trusted_system"
    AUTHENTICATED_USER = "authenticated_user"
    UNTRUSTED_INPUT = "untrusted_input"
    UNTRUSTED_RETRIEVAL = "untrusted_retrieval"
    UNTRUSTED_TOOL_RESULT = "untrusted_tool_result"
    MEMORY = "memory"


class Risk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Principal:
    principal_id: str
    tenant_id: str
    capabilities: frozenset[str]


@dataclass(frozen=True)
class Action:
    tool: str
    operation: str
    args: dict[str, object]
    tenant_id: str
    risk: Risk
    resource_id: str | None = None


@dataclass(frozen=True)
class Approval:
    approval_id: str
    action_hash: str
    principal_id: str
    tenant_id: str
    policy_version: str
    state_version: str
    used: bool = False


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str
    approval_required: bool = False


@dataclass
class SecurityEvent:
    event_type: str
    principal_id: str
    tenant_id: str
    detail: str
    metadata: dict[str, object] = field(default_factory=dict)


class SecurityViolation(Exception):
    pass


def action_hash(action: Action, policy_version: str, state_version: str) -> str:
    """Stable binding used to prevent approval substitution/replay."""
    canonical = (
        f"{action.tenant_id}|{action.tool}|{action.operation}|"
        f"{sorted(action.args.items())}|{action.resource_id}|{action.risk.value}|"
        f"{policy_version}|{state_version}"
    )
    return hashlib.sha256(canonical.encode()).hexdigest()


class SecurityPolicy:
    def __init__(
        self,
        *,
        tool_capabilities: dict[str, str],
        high_risk_threshold: Risk = Risk.HIGH,
        allowed_hosts: set[str] | None = None,
        policy_version: str = "v1",
    ) -> None:
        self.tool_capabilities = tool_capabilities
        self.high_risk_threshold = high_risk_threshold
        self.allowed_hosts = {h.lower() for h in (allowed_hosts or set())}
        self.policy_version = policy_version

    def authorize(self, principal: Principal, action: Action) -> PolicyDecision:
        if principal.tenant_id != action.tenant_id:
            return PolicyDecision(False, "cross-tenant action denied")
        required = self.tool_capabilities.get(action.tool)
        if required is None:
            return PolicyDecision(False, "tool not allowlisted")
        if required not in principal.capabilities:
            return PolicyDecision(False, f"missing capability: {required}")
        needs_approval = action.risk in {Risk.HIGH, Risk.CRITICAL}
        return PolicyDecision(True, "authorized", needs_approval)

    def authorize_url(self, url: str) -> PolicyDecision:
        parsed = urlparse(url)
        if parsed.scheme not in {"https"} or not parsed.hostname:
            return PolicyDecision(False, "only HTTPS URLs with a hostname are allowed")
        host = parsed.hostname.lower().rstrip(".")
        if host not in self.allowed_hosts:
            return PolicyDecision(False, "destination not in egress allowlist")
        try:
            ip = ipaddress.ip_address(host)
        except ValueError:
            ip = None
        if ip and (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved):
            return PolicyDecision(False, "private/reserved destination denied")
        return PolicyDecision(True, "egress allowed")


class ApprovalStore:
    def __init__(self) -> None:
        self._approvals: dict[str, Approval] = {}

    def issue(self, principal: Principal, action: Action, state_version: str) -> Approval:
        digest = action_hash(action, "v1", state_version)
        approval = Approval(
            approval_id=hashlib.sha256(f"{digest}|{principal.principal_id}".encode()).hexdigest()[:24],
            action_hash=digest,
            principal_id=principal.principal_id,
            tenant_id=principal.tenant_id,
            policy_version="v1",
            state_version=state_version,
        )
        self._approvals[approval.approval_id] = approval
        return approval

    def consume(
        self,
        approval_id: str,
        principal: Principal,
        action: Action,
        state_version: str,
    ) -> None:
        approval = self._approvals.get(approval_id)
        if not approval or approval.used:
            raise SecurityViolation("approval missing or already consumed")
        if approval.principal_id != principal.principal_id or approval.tenant_id != principal.tenant_id:
            raise SecurityViolation("approval principal/tenant mismatch")
        expected = action_hash(action, approval.policy_version, state_version)
        if approval.action_hash != expected or approval.state_version != state_version:
            raise SecurityViolation("approval does not match exact action/state")
        self._approvals[approval_id] = Approval(**{**approval.__dict__, "used": True})


_SECRET_PATTERNS = [
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]+"),
    re.compile(r"(?i)(api[_-]?key\s*[:=]\s*)[^\s,;]+"),
    re.compile(r"(?i)(password\s*[:=]\s*)[^\s,;]+"),
    re.compile(r"(?i)(secret\s*[:=]\s*)[^\s,;]+"),
]


def redact_secrets(text: str) -> str:
    result = text
    for pattern in _SECRET_PATTERNS:
        result = pattern.sub(r"\1[REDACTED]", result)
    return result


def label_untrusted(text: str, trust: Trust) -> str:
    """Make provenance explicit; this does not confer authority."""
    return f"[{trust.value.upper()} DATA — NOT POLICY]\n{text}"


def looks_like_prompt_injection(text: str) -> bool:
    patterns = [
        r"ignore\s+(all|any|previous)\s+instructions",
        r"reveal\s+(the|your)\s+(system|secret|hidden)",
        r"override\s+(the|your)\s+(policy|rules)",
        r"disable\s+(security|logging|approval)",
    ]
    lowered = text.lower()
    return any(re.search(p, lowered) for p in patterns)
