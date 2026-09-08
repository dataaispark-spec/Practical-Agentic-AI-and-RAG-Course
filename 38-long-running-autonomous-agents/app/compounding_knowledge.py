"""Karpathy-inspired compounding-knowledge primitives.

Educational baseline: deterministic updates, provenance, supersession and
contradiction recording. No claim is promoted to trusted knowledge silently.
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class KnowledgeItem:
    item_id: str
    subject: str
    predicate: str
    object: str
    source_id: str
    version: int = 1
    status: str = "active"


@dataclass
class KnowledgeBase:
    items: dict[str, KnowledgeItem] = field(default_factory=dict)
    contradictions: list[tuple[str, str]] = field(default_factory=list)

    def upsert(self, item: KnowledgeItem) -> str:
        existing = next((x for x in self.items.values() if x.subject == item.subject and x.predicate == item.predicate and x.status == "active"), None)
        if existing and existing.object != item.object:
            self.contradictions.append((existing.item_id, item.item_id))
            return "contradiction"
        if existing:
            return "duplicate"
        self.items[item.item_id] = item
        return "added"

    def supersede(self, old_id: str, replacement: KnowledgeItem) -> None:
        old = self.items[old_id]
        self.items[old_id] = KnowledgeItem(old.item_id, old.subject, old.predicate, old.object, old.source_id, old.version, "superseded")
        self.items[replacement.item_id] = replacement

    def trusted(self, item_id: str) -> KnowledgeItem:
        item = self.items[item_id]
        if item.status != "active" or not item.source_id:
            raise ValueError("knowledge item is not trusted/active")
        return item

    def health(self) -> dict[str, int]:
        return {
            "items": len(self.items),
            "active": sum(i.status == "active" for i in self.items.values()),
            "contradictions": len(self.contradictions),
            "provenance_missing": sum(not i.source_id for i in self.items.values()),
        }
