"""Small, deterministic GraphRAG benchmark primitive for Module 32."""
from dataclasses import dataclass
from math import inf


@dataclass(frozen=True)
class GraphHit:
    entity_id: str
    score: float
    path: tuple[str, ...]
    claim_ids: tuple[str, ...]


def bounded_graph_retrieve(graph, start: str, tenant_id: str, max_hops: int = 2, max_hits: int = 8) -> list[GraphHit]:
    if max_hits <= 0:
        return []
    if max_hops < 0 or max_hops > 5:
        raise ValueError("max_hops must be between 0 and 5")
    if start not in graph.entities or graph.entities[start].tenant_id != tenant_id:
        return []

    distances = {start: 0}
    queue = [start]
    while queue:
        current = queue.pop(0)
        if distances[current] >= max_hops:
            continue
        for edge in graph.edges:
            if edge.tenant_id != tenant_id:
                continue
            nxt = edge.target_id if edge.source_id == current else edge.source_id if edge.target_id == current else None
            if nxt and nxt not in distances:
                distances[nxt] = distances[current] + 1
                queue.append(nxt)

    hits = []
    for entity_id, distance in distances.items():
        if entity_id == start:
            continue
        claim_ids = tuple(sorted(
            c.claim_id for c in graph.claims.values()
            if c.tenant_id == tenant_id and (c.subject_id == entity_id or c.object_id == entity_id)
        ))
        hits.append(GraphHit(entity_id, 1.0 / max(distance, 1), (start, entity_id), claim_ids))
    hits.sort(key=lambda h: (-h.score, h.entity_id))
    return hits[:max_hits]


def reciprocal_rank_fusion(graph_hits: list[GraphHit], vector_ids: list[str], k: int = 60) -> list[str]:
    scores: dict[str, float] = {}
    for rank, hit in enumerate(graph_hits, 1):
        scores[hit.entity_id] = scores.get(hit.entity_id, 0.0) + 1.0 / (k + rank)
    for rank, entity_id in enumerate(vector_ids, 1):
        scores[entity_id] = scores.get(entity_id, 0.0) + 1.0 / (k + rank)
    return [entity_id for entity_id, _ in sorted(scores.items(), key=lambda item: (-item[1], item[0]))]
