"""Graph-aware observation primitives for Module 31.

The graph is treated as bounded evidence, not authority. The loop receives a
small neighborhood plus provenance summaries and must still pass policy and
verification before acting.
"""
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GraphObservation:
    query_entity: str
    tenant_id: str
    hops: int
    entities: tuple[dict[str, Any], ...]
    evidence_claim_ids: tuple[str, ...]


def build_graph_observation(graph, entity_id: str, tenant_id: str, hops: int = 1) -> GraphObservation:
    entities = graph.neighbors(entity_id, tenant_id, hops)
    payload = tuple(
        {"entity_id": e.entity_id, "type": e.entity_type, "name": e.name}
        for e in entities
    )
    ids = tuple(
        sorted(
            c.claim_id
            for c in graph.claims.values()
            if c.tenant_id == tenant_id
            and (c.subject_id == entity_id or c.object_id in {e.entity_id for e in entities})
        )
    )
    return GraphObservation(entity_id, tenant_id, hops, payload, ids)
