from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Entity:
    entity_id: str
    entity_type: str
    name: str
    tenant_id: str

@dataclass(frozen=True)
class Edge:
    source: str
    relation: str
    target: str
    tenant_id: str
    provenance: str

class KnowledgeGraph:
    def __init__(self) -> None:
        self.entities: dict[str, Entity] = {}
        self.edges: list[Edge] = []

    def add_entity(self, entity: Entity) -> None:
        self.entities[entity.entity_id] = entity

    def add_edge(self, edge: Edge) -> None:
        if not edge.provenance:
            raise ValueError("provenance is required")
        if edge.source not in self.entities or edge.target not in self.entities:
            raise ValueError("edge endpoint is unknown")
        if self.entities[edge.source].tenant_id != edge.tenant_id or self.entities[edge.target].tenant_id != edge.tenant_id:
            raise PermissionError("cross-tenant edge")
        self.edges.append(edge)

    def neighbors(self, entity_id: str, tenant_id: str, depth: int = 1) -> set[str]:
        if depth < 0 or depth > 3:
            raise ValueError("depth must be between 0 and 3")
        seen = {entity_id}
        frontier = {entity_id}
        for _ in range(depth):
            nxt = set()
            for e in self.edges:
                if e.tenant_id != tenant_id:
                    continue
                if e.source in frontier:
                    nxt.add(e.target)
                if e.target in frontier:
                    nxt.add(e.source)
            nxt -= seen
            seen |= nxt
            frontier = nxt
        return seen

    def edges_for(self, entity_ids: Iterable[str], tenant_id: str) -> list[Edge]:
        ids = set(entity_ids)
        return [e for e in self.edges if e.tenant_id == tenant_id and e.source in ids and e.target in ids]
