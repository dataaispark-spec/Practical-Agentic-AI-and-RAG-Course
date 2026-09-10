from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Proposal:
    subject: str
    predicate: str
    object: str
    source_id: str
    tenant_id: str
    confidence: float
    risk: str = "low"

    @property
    def proposal_id(self) -> str:
        payload = json.dumps(self.__dict__, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode()).hexdigest()


def validate(proposal: Proposal, known_entities: set[str], allowed_predicates: set[str]) -> None:
    if not 0.0 <= proposal.confidence <= 1.0:
        raise ValueError("confidence must be in [0, 1]")
    if proposal.subject not in known_entities or proposal.object not in known_entities:
        raise ValueError("proposal references unknown entity")
    if proposal.predicate not in allowed_predicates:
        raise ValueError("unsupported predicate")
    if not proposal.source_id:
        raise ValueError("provenance is required")
    if not proposal.tenant_id:
        raise ValueError("tenant is required")


def approval_required(proposal: Proposal, threshold: set[str] = frozenset({"high", "critical"})) -> bool:
    return proposal.risk in threshold
