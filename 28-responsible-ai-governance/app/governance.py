from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    APPROVAL_REQUIRED = "approval_required"
    REVIEW = "review"


@dataclass(frozen=True)
class UseCase:
    use_case_id: str
    tenant_id: str
    purpose: str
    risk_tier: int
    data_class: str
    model: str
    tool: str | None = None
    human_oversight: bool = False


@dataclass(frozen=True)
class GovernancePolicy:
    allowed_models: frozenset[str]
    allowed_tools: frozenset[str]
    max_risk_without_approval: int = 1
    allowed_data_classes: frozenset[str] = frozenset({"public", "internal"})


@dataclass(frozen=True)
class GovernanceDecision:
    decision: Decision
    reason: str
    action_hash: str


def action_hash(use_case: UseCase) -> str:
    payload = json.dumps(use_case.__dict__, sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode()).hexdigest()


def evaluate(use_case: UseCase, policy: GovernancePolicy) -> GovernanceDecision:
    digest = action_hash(use_case)
    if use_case.model not in policy.allowed_models:
        return GovernanceDecision(Decision.DENY, "model_not_approved", digest)
    if use_case.data_class not in policy.allowed_data_classes:
        return GovernanceDecision(Decision.DENY, "data_class_not_allowed", digest)
    if use_case.tool and use_case.tool not in policy.allowed_tools:
        return GovernanceDecision(Decision.DENY, "tool_not_approved", digest)
    if use_case.risk_tier > policy.max_risk_without_approval:
        if use_case.human_oversight:
            return GovernanceDecision(Decision.APPROVAL_REQUIRED, "high_risk_human_gate", digest)
        return GovernanceDecision(Decision.DENY, "high_risk_requires_human_oversight", digest)
    return GovernanceDecision(Decision.ALLOW, "policy_satisfied", digest)
