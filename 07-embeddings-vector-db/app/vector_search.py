from __future__ import annotations

from dataclasses import dataclass
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


def deterministic_embedding(text: str, dimensions: int = 128) -> tuple[float, ...]:
    if dimensions <= 0:
        raise ValueError("dimensions must be positive")
    vector = [0.0] * dimensions
    for token in tokenize(text):
        vector[hash(token) % dimensions] += 1.0
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
        self._records.extend(records)

    def search(self, query_vector: tuple[float, ...], k: int = 5, tenant_id: str | None = None) -> list[tuple[VectorRecord, float]]:
        if k < 1:
            return []
        candidates = []
        for record in self._records:
            if tenant_id is not None and record.tenant_id != tenant_id:
                continue
            score = cosine(query_vector, record.vector)
            candidates.append((record, score))
        candidates.sort(key=lambda pair: pair[1], reverse=True)
        return candidates[:k]


def recall_at_k(ground_truth: list[str], predicted: list[str], k: int) -> float:
    expected = set(ground_truth[:k])
    if not expected:
        return 0.0
    return len(expected.intersection(predicted[:k])) / len(expected)
