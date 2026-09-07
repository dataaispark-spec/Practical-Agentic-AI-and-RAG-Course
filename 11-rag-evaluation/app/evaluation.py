from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import math

@dataclass(frozen=True)
class EvalCase:
    case_id: str
    query: str
    relevant_docs: frozenset[str]
    expected_answer: str
    answerable: bool = True

@dataclass(frozen=True)
class EvalResult:
    case_id: str
    recall_at_k: float
    mrr: float
    answer_exact_match: float
    grounded: float


def recall_at_k(ranked_ids: Iterable[str], relevant: set[str], k: int) -> float:
    ids = list(ranked_ids)[:k]
    return len(set(ids) & relevant) / max(len(relevant), 1)


def reciprocal_rank(ranked_ids: Iterable[str], relevant: set[str]) -> float:
    for i, doc_id in enumerate(ranked_ids, 1):
        if doc_id in relevant:
            return 1.0 / i
    return 0.0


def exact_match(predicted: str, expected: str) -> float:
    return float(predicted.strip().casefold() == expected.strip().casefold())


def groundedness(supporting_doc_ids: Iterable[str], cited_doc_ids: Iterable[str]) -> float:
    support = set(supporting_doc_ids)
    cited = set(cited_doc_ids)
    if not cited:
        return 0.0
    return len(cited & support) / len(cited)


def mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / max(len(values), 1)


def bootstrap_mean(values: list[float], iterations: int = 500, seed: int = 7) -> tuple[float, float]:
    import random
    rng = random.Random(seed)
    if not values:
        return 0.0, 0.0
    samples = []
    for _ in range(iterations):
        sample = [rng.choice(values) for _ in values]
        samples.append(mean(sample))
    samples.sort()
    return samples[int(0.025 * len(samples))], samples[int(0.975 * len(samples))]


def regression_gate(baseline: float, candidate: float, max_drop: float = 0.02) -> bool:
    return candidate >= baseline - max_drop
