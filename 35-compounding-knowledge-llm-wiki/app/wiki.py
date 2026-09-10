"""Deterministic reference implementation for compounding knowledge.

The implementation is deliberately framework-free so learners can inspect the
mechanism before introducing databases, LLMs or graph frameworks.
"""
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    source: str
    content_hash: str
    tenant: str = "default"
    observed_at: str = ""
    authority: float = 0.5

    @staticmethod
    def from_text(evidence_id: str, source: str, text: str, tenant: str = "default", observed_at: str = "", authority: float = 0.5) -> "Evidence":
        if not source or not text:
            raise ValueError("source and evidence text are required")
        return Evidence(evidence_id, source, sha256(text.encode()).hexdigest(), tenant, observed_at, max(0.0, min(1.0, authority)))


@dataclass(frozen=True)
class Claim:
    topic: str
    text: str
    source: str
    version: int = 1
    claim_id: str = ""
    evidence_id: str = ""
    tenant: str = "default"
    confidence: float = 1.0
    status: str = "ACTIVE"
    observed_at: str = ""
    valid_from: str = ""
    valid_to: str = ""

    def identity(self) -> str:
        return self.claim_id or sha256(f"{self.tenant}|{self.topic}|{self.text}|{self.evidence_id}".encode()).hexdigest()[:16]


@dataclass(frozen=True)
class Change:
    action: str
    claim_id: str
    topic: str
    version: int
    reason: str


@dataclass
class Wiki:
    """Small deterministic knowledge lifecycle: validate, promote, supersede, rollback."""
    claims: Dict[str, List[Claim]] = field(default_factory=dict)
    evidence: Dict[str, Evidence] = field(default_factory=dict)
    changes: List[Change] = field(default_factory=list)
    quarantined: List[Claim] = field(default_factory=list)

    def register_evidence(self, item: Evidence) -> Evidence:
        self.evidence[item.evidence_id] = item
        return item

    def _validate(self, claim: Claim) -> None:
        if not claim.topic.strip() or not claim.text.strip() or not claim.source.strip():
            raise ValueError("topic, text and source are required")
        if not 0.0 <= claim.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if claim.evidence_id:
            evidence = self.evidence.get(claim.evidence_id)
            if evidence is None:
                raise ValueError("claim references unknown evidence")
            if evidence.tenant != claim.tenant:
                raise PermissionError("cross-tenant evidence reference denied")

    def upsert(self, claim: Claim, reason: str = "validated update") -> Claim:
        self._validate(claim)
        cid = claim.identity()
        history = self.claims.setdefault(claim.topic, [])
        current = self.active(claim.topic, tenant=claim.tenant)
        if current and current.text == claim.text and current.evidence_id == claim.evidence_id:
            return current
        if current:
            superseded = Claim(**{**current.__dict__, "status": "SUPERSEDED", "valid_to": claim.observed_at or current.valid_to, "version": current.version})
            history[history.index(current)] = superseded
            self.changes.append(Change("SUPERSEDE", current.identity(), current.topic, current.version, reason))
        next_version = (max((c.version for c in history if c.tenant == claim.tenant), default=0) + 1)
        promoted = Claim(**{**claim.__dict__, "claim_id": cid, "version": next_version, "status": "ACTIVE"})
        history.append(promoted)
        self.changes.append(Change("PROMOTE", cid, claim.topic, next_version, reason))
        return promoted

    def quarantine(self, claim: Claim, reason: str = "failed validation") -> Claim:
        self.quarantined.append(claim)
        self.changes.append(Change("QUARANTINE", claim.identity(), claim.topic, claim.version, reason))
        return claim

    def active(self, topic: str, tenant: str = "default") -> Optional[Claim]:
        candidates = [c for c in self.claims.get(topic, []) if c.tenant == tenant and c.status == "ACTIVE"]
        return candidates[-1] if candidates else None

    def contradictions(self, topic: str, tenant: str = "default") -> List[Claim]:
        active = self.active(topic, tenant)
        if not active:
            return []
        return [c for c in self.claims.get(topic, []) if c.tenant == tenant and c.status == "CONTRADICTED"]

    def mark_contradiction(self, claim_id: str, reason: str = "conflicting evidence") -> bool:
        for topic, history in self.claims.items():
            for i, claim in enumerate(history):
                if claim.identity() == claim_id and claim.status == "ACTIVE":
                    history[i] = Claim(**{**claim.__dict__, "status": "CONTRADICTED"})
                    self.changes.append(Change("CONTRADICT", claim_id, topic, claim.version, reason))
                    return True
        return False

    def rollback(self, topic: str, version: int, tenant: str = "default", reason: str = "rollback") -> Claim:
        history = self.claims.get(topic, [])
        target = next((c for c in history if c.tenant == tenant and c.version == version), None)
        if target is None:
            raise KeyError(f"unknown version {version} for {topic}")
        current = self.active(topic, tenant)
        if current and current.identity() != target.identity():
            idx = history.index(current)
            history[idx] = Claim(**{**current.__dict__, "status": "ROLLED_BACK"})
        restored = Claim(**{**target.__dict__, "status": "ACTIVE"})
        idx = history.index(target)
        history[idx] = restored
        self.changes.append(Change("ROLLBACK", restored.identity(), topic, restored.version, reason))
        return restored

    def page(self, topic: str, tenant: str = "default") -> str:
        c = self.active(topic, tenant)
        if not c:
            return "UNKNOWN"
        provenance = f"source={c.source}; evidence={c.evidence_id or 'none'}; version={c.version}; confidence={c.confidence:.2f}; status={c.status}"
        return f"{c.text} [{provenance}]"

    def compile_context(self, topics: Iterable[str], tenant: str = "default", max_chars: int = 1200) -> str:
        parts: List[str] = []
        for topic in topics:
            page = self.page(topic, tenant)
            if page != "UNKNOWN":
                parts.append(f"[{topic}] {page}")
        return "\n".join(parts)[:max_chars]

    def provenance_coverage(self, tenant: str = "default") -> float:
        active = [c for hs in self.claims.values() for c in hs if c.tenant == tenant and c.status == "ACTIVE"]
        return sum(bool(c.evidence_id) for c in active) / len(active) if active else 1.0

    def health(self, tenant: str = "default") -> Dict[str, float]:
        active = [c for hs in self.claims.values() for c in hs if c.tenant == tenant and c.status == "ACTIVE"]
        topics = {c.topic for c in active}
        return {
            "active_claims": float(len(active)),
            "topics": float(len(topics)),
            "provenance_coverage": self.provenance_coverage(tenant),
            "quarantine_count": float(len([c for c in self.quarantined if c.tenant == tenant])),
            "change_count": float(len(self.changes)),
        }
