from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class Entity:
    entity_id: str
    entity_type: str
    name: str
    tenant_id: str
    source_ids: tuple[str, ...] = ()
    attributes: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Claim:
    claim_id: str
    subject_id: str
    predicate: str
    object_id: str | None
    text: str
    source_id: str
    tenant_id: str
    confidence: float = 1.0
    valid_from: str | None = None
    valid_to: str | None = None


@dataclass(frozen=True)
class Edge:
    source_id: str
    relation: str
    target_id: str
    claim_id: str
    tenant_id: str
    confidence: float = 1.0
    valid_from: str | None = None
    valid_to: str | None = None


class GraphValidationError(ValueError):
    pass


@dataclass
class KnowledgeGraph:
    entities: dict[str, Entity] = field(default_factory=dict)
    claims: dict[str, Claim] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)

    def add_entity(self, entity: Entity) -> None:
        if entity.entity_id in self.entities:
            old = self.entities[entity.entity_id]
            if old.tenant_id != entity.tenant_id or old.entity_type != entity.entity_type:
                raise GraphValidationError("entity identity collision")
            return
        self.entities[entity.entity_id] = entity

    def add_claim(self, claim: Claim) -> None:
        if not 0.0 <= claim.confidence <= 1.0:
            raise GraphValidationError("confidence must be in [0, 1]")
        if claim.tenant_id != self.entities.get(claim.subject_id, Entity("", "", "", "")).tenant_id:
            raise GraphValidationError("claim/entity tenant mismatch")
        if claim.object_id and claim.object_id not in self.entities:
            raise GraphValidationError("claim references unknown object")
        if claim.claim_id in self.claims:
            raise GraphValidationError("duplicate claim id")
        self.claims[claim.claim_id] = claim

    def add_edge(self, edge: Edge) -> None:
        if edge.source_id not in self.entities or edge.target_id not in self.entities:
            raise GraphValidationError("edge references unknown entity")
        if self.entities[edge.source_id].tenant_id != edge.tenant_id or self.entities[edge.target_id].tenant_id != edge.tenant_id:
            raise GraphValidationError("cross-tenant edge denied")
        if edge.claim_id not in self.claims:
            raise GraphValidationError("edge requires provenance claim")
        if not 0.0 <= edge.confidence <= 1.0:
            raise GraphValidationError("confidence must be in [0, 1]")
        if any(e.source_id == edge.source_id and e.relation == edge.relation and e.target_id == edge.target_id and e.valid_from == edge.valid_from and e.valid_to == edge.valid_to for e in self.edges):
            return
        self.edges.append(edge)

    def neighbors(self, entity_id: str, tenant_id: str, max_hops: int = 1) -> list[Entity]:
        if max_hops < 0 or max_hops > 5:
            raise GraphValidationError("max_hops must be between 0 and 5")
        if entity_id not in self.entities or self.entities[entity_id].tenant_id != tenant_id:
            return []
        seen = {entity_id}
        frontier = {entity_id}
        for _ in range(max_hops):
            nxt: set[str] = set()
            for edge in self.edges:
                if edge.tenant_id != tenant_id:
                    continue
                if edge.source_id in frontier and edge.target_id not in seen:
                    nxt.add(edge.target_id)
                if edge.target_id in frontier and edge.source_id not in seen:
                    nxt.add(edge.source_id)
            seen |= nxt
            frontier = nxt
        return [self.entities[i] for i in sorted(seen - {entity_id})]

    def validate(self) -> list[str]:
        errors: list[str] = []
        for edge in self.edges:
            try:
                self.add_edge(edge)
            except GraphValidationError as exc:
                errors.append(str(exc))
        return errors

    def degree(self, entity_id: str) -> int:
        return sum(e.source_id == entity_id or e.target_id == entity_id for e in self.edges)
