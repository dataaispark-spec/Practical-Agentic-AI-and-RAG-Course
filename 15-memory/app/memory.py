from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import re
from typing import Iterable

@dataclass(frozen=True)
class Memory:
    memory_id: str
    tenant_id: str
    kind: str
    content: str
    source: str
    confidence: float = 1.0
    importance: float = 0.5
    expires_at: datetime | None = None
    version: int = 1
    supersedes: str | None = None

class MemoryStore:
    def __init__(self) -> None:
        self._items: dict[str, Memory] = {}

    def put(self, memory: Memory) -> None:
        if not 0 <= memory.confidence <= 1 or not 0 <= memory.importance <= 1:
            raise ValueError('confidence and importance must be between 0 and 1')
        self._items[memory.memory_id] = memory

    def delete(self, memory_id: str) -> None:
        self._items.pop(memory_id, None)

    def get(self, memory_id: str, tenant_id: str, now: datetime | None = None) -> Memory | None:
        item = self._items.get(memory_id)
        if not item or item.tenant_id != tenant_id:
            return None
        if item.expires_at and item.expires_at <= (now or datetime.now(timezone.utc)):
            return None
        return item

    def search(self, query: str, tenant_id: str, k: int = 5, now: datetime | None = None) -> list[Memory]:
        now = now or datetime.now(timezone.utc)
        q = set(re.findall(r"\w+", query.lower()))
        scored: list[tuple[float, Memory]] = []
        for m in self._items.values():
            if m.tenant_id != tenant_id or (m.expires_at and m.expires_at <= now):
                continue
            words = set(re.findall(r"\w+", m.content.lower()))
            relevance = len(q & words) / max(1, len(q))
            score = relevance * m.confidence * (0.5 + 0.5 * m.importance)
            if score > 0:
                scored.append((score, m))
        return [m for _, m in sorted(scored, key=lambda x: x[0], reverse=True)[:k]]

    def contradicts(self, candidate: Memory, existing: Iterable[Memory]) -> list[Memory]:
        # Educational heuristic: same tenant/kind/source topic with different content.
        return [m for m in existing if m.tenant_id == candidate.tenant_id and m.kind == candidate.kind and m.content != candidate.content]

def ttl_memory(memory_id: str, tenant_id: str, kind: str, content: str, source: str, days: int) -> Memory:
    return Memory(memory_id, tenant_id, kind, content, source, expires_at=datetime.now(timezone.utc) + timedelta(days=days))
