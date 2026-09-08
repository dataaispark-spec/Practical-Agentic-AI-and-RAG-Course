from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
import re
from typing import Iterable


@dataclass(frozen=True)
class Document:
    document_id: str
    text: str
    tenant_id: str = "default"
    version: str = "1"
    source: str = "unknown"
    effective_at: str | None = None
    acl: tuple[str, ...] = ()


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    text: str
    tenant_id: str
    version: str
    source: str
    effective_at: str | None = None
    acl: tuple[str, ...] = ()


@dataclass(frozen=True)
class Evidence:
    chunk: Chunk
    score: float


def chunk_document(document: Document, size: int = 500, overlap: int = 50) -> list[Chunk]:
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("require size > 0 and 0 <= overlap < size")
    words = document.text.split()
    chunks: list[Chunk] = []
    step = size - overlap
    for start in range(0, len(words), step):
        text = " ".join(words[start : start + size]).strip()
        if not text:
            break
        chunks.append(Chunk(
            chunk_id=f"{document.document_id}#chunk-{len(chunks):04d}",
            document_id=document.document_id,
            text=text,
            tenant_id=document.tenant_id,
            version=document.version,
            source=document.source,
            effective_at=document.effective_at,
            acl=document.acl,
        ))
        if start + size >= len(words):
            break
    return chunks


def _bucket(token: str, dimensions: int) -> int:
    return int.from_bytes(hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest(), "big") % dimensions


def _embed(text: str, dimensions: int = 256) -> list[float]:
    """Stable offline embedding for reproducible teaching and CI."""
    vector = [0.0] * dimensions
    for token in re.findall(r"\w+", text.lower()):
        vector[_bucket(token, dimensions)] += 1.0
    norm = math.sqrt(sum(x * x for x in vector))
    return [x / norm for x in vector] if norm else vector


def cosine(a: Iterable[float], b: Iterable[float]) -> float:
    av, bv = list(a), list(b)
    if len(av) != len(bv):
        raise ValueError("vectors must have equal dimensions")
    na = math.sqrt(sum(x * x for x in av))
    nb = math.sqrt(sum(x * x for x in bv))
    if not na or not nb:
        return 0.0
    return sum(x * y for x, y in zip(av, bv)) / (na * nb)


class VectorIndex:
    def __init__(self) -> None:
        self._items: list[tuple[Chunk, list[float]]] = []

    def add(self, chunks: Iterable[Chunk]) -> None:
        for chunk in chunks:
            if not chunk.tenant_id:
                raise ValueError("chunk tenant_id is required")
            if not chunk.acl:
                raise ValueError("chunk ACL is required")
            self._items.append((chunk, _embed(chunk.text)))

    def search(self, query: str, k: int = 5, tenant_id: str | None = None, principal: str | None = None) -> list[Evidence]:
        if k <= 0:
            return []
        if not tenant_id or not principal:
            raise ValueError("tenant_id and principal are required for authorized search")
        q = _embed(query)
        candidates = [
            (chunk, cosine(q, vector))
            for chunk, vector in self._items
            if chunk.tenant_id == tenant_id and principal in chunk.acl
        ]
        candidates.sort(key=lambda item: (-item[1], item[0].chunk_id))
        return [Evidence(chunk=c, score=s) for c, s in candidates[:k]]


def build_context(evidence: Iterable[Evidence]) -> str:
    return "\n\n".join(f"[{item.chunk.chunk_id}] {item.chunk.text}" for item in evidence)


def should_abstain(evidence: list[Evidence], minimum_score: float = 0.05) -> bool:
    return not evidence or max(item.score for item in evidence) < minimum_score
