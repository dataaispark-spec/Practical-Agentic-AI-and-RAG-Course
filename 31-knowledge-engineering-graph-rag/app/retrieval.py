from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from .graph import KnowledgeGraph


@dataclass(frozen=True)
class EvidencePath:
    nodes: tuple[str, ...]
    relations: tuple[str, ...]
    provenance: tuple[str, ...]


def shortest_paths(graph: KnowledgeGraph, start: str, target: str, tenant_id: str, max_hops: int = 3) -> list[EvidencePath]:
    if max_hops < 1 or max_hops > 5:
        raise ValueError("max_hops must be between 1 and 5")
    queue = deque([(start, (start,), (), ())])
    paths: list[EvidencePath] = []
    while queue:
        node, nodes, relations, provenance = queue.popleft()
        if node == target and len(nodes) > 1:
            paths.append(EvidencePath(nodes, relations, provenance))
            continue
        if len(relations) >= max_hops:
            continue
        for edge in graph.edges:
            if edge.tenant_id != tenant_id:
                continue
            if edge.source == node:
                nxt, rel = edge.target, edge.relation
            elif edge.target == node:
                nxt, rel = edge.source, edge.relation
            else:
                continue
            if nxt in nodes:
                continue
            queue.append((nxt, nodes + (nxt,), relations + (rel,), provenance + (edge.provenance,)))
    return paths
