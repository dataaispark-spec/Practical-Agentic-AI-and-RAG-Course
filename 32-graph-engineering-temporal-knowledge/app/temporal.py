from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class TemporalEdge:
    source: str
    relation: str
    target: str
    valid_from: date
    valid_to: date | None
    provenance: str

    def active_on(self, when: date) -> bool:
        return self.valid_from <= when and (self.valid_to is None or when <= self.valid_to)

def detect_overlap(edges: list[TemporalEdge]) -> list[tuple[TemporalEdge, TemporalEdge]]:
    out=[]
    for i,a in enumerate(edges):
        for b in edges[i+1:]:
            if (a.source,a.relation,a.target)!=(b.source,b.relation,b.target): continue
            a_end=a.valid_to or date.max; b_end=b.valid_to or date.max
            if max(a.valid_from,b.valid_from) <= min(a_end,b_end): out.append((a,b))
    return out
