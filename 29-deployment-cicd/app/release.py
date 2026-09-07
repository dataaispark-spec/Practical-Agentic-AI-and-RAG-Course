from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class GateStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    BLOCK = "block"


@dataclass(frozen=True)
class ReleaseManifest:
    application: str
    application_version: str
    artifact_digest: str
    model_version: str
    prompt_version: str
    retrieval_version: str
    policy_version: str
    evaluation_version: str


@dataclass(frozen=True)
class Gate:
    name: str
    status: GateStatus
    reason: str = ""


def validate_manifest(m: ReleaseManifest) -> list[str]:
    required = {
        "application": m.application,
        "application_version": m.application_version,
        "artifact_digest": m.artifact_digest,
        "model_version": m.model_version,
        "prompt_version": m.prompt_version,
        "retrieval_version": m.retrieval_version,
        "policy_version": m.policy_version,
        "evaluation_version": m.evaluation_version,
    }
    return [name for name, value in required.items() if not value]


def release_status(gates: list[Gate]) -> GateStatus:
    if any(g.status is GateStatus.BLOCK for g in gates):
        return GateStatus.BLOCK
    if any(g.status is GateStatus.WARN for g in gates):
        return GateStatus.WARN
    return GateStatus.PASS
