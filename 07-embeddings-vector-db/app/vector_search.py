from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
import re
from typing import Iterable


@dataclass(frozen=True)
class VectorRecord:
    record_id: str
    text: str
    vector: tuple[float, ...]
    tenant_id: str
    embedding_model: str
    index_version: str


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def _stable_bucket(token: str, dimensions: int) -> int:
    digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "big") % dimensions


def deterministic_embedding(text: str, dimensions: int = 128) -> tuple[float, ...]:
    """Reproducible toy embedding; unlike Python hash(), stable across processes."""
    if dimensions <= 0:
        raise ValueError("dimensions must be positive")
    vector = [0.0] * dimensions
    for token in tokenize(text):
        vector[_stable_bucket(token, dimensions)] += 1.0
    norm = math.sqrt(sum(value * value for value in vector))
    if norm:
        vector = [value / norm for value in vector]
    return tuple(vector)


def cosine(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    if len(a) != len(b):
        raise ValueError("vectors must have equal dimensions")
    return sum(x * y for x, y in zip(a, b))


class ExactVectorIndex:
    """Educational exact-search reference implementation."""

    def __init__(self) -> None:
        self._records: list[VectorRecord] = []

    def add(self, records: Iterable[VectorRecord]) -> None:
        for record in records:
            if not record.tenant_id:
                raise ValueError("tenant_id is required")
            if not record.embedding_model or not record.index_version:
                raise ValueError("embedding_model and index_version are required")
            self._records.append(record)

    def search(self, query_vector: tuple[float, ...], k: int = 5, tenant_id: str | None = None) -> list[tuple[VectorRecord, float]]:
        if k < 1:
            return []
        candidates = []
        for record in self._records:
            if tenant_id is not None and record.tenant_id != tenant_id:
                continue
            score = cosine(query_vector, record.vector)
            candidates.append((record, score))
        candidates.sort(key=lambda pair: (-pair[1], pair[0].record_id))
        return candidates[:k]


def recall_at_k(ground_truth: list[str], predicted: list[str], k: int) -> float:
    """Recall against all labeled relevant IDs, considering the predicted top-k."""
    if k < 1 or not ground_truth:
        return 0.0
    relevant = set(ground_truth)
    retrieved = set(predicted[:k])
    return len(relevant.intersection(retrieved)) / len(relevant)
