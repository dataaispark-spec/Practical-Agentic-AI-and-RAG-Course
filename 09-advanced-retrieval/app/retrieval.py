from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
import math
import re
from typing import Iterable

TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+")

@dataclass(frozen=True)
class Doc:
    doc_id: str
    text: str
    metadata: dict[str, str]

@dataclass(frozen=True)
class Hit:
    doc_id: str
    score: float
    method: str


def tokenize(text: str) -> list[str]:
    return [x.lower() for x in TOKEN_RE.findall(text)]


def bm25(docs: list[Doc], query: str, k: int = 5, k1: float = 1.5, b: float = 0.75) -> list[Hit]:
    q = tokenize(query)
    if not q or not docs:
        return []
    lengths = [len(tokenize(d.text)) for d in docs]
    avgdl = sum(lengths) / max(len(lengths), 1)
    df = Counter()
    for d in docs:
        df.update(set(tokenize(d.text)))
    n = len(docs)
    hits = []
    for d, dl in zip(docs, lengths):
        tf = Counter(tokenize(d.text))
        score = 0.0
        for term in q:
            if term not in tf:
                continue
            idf = math.log(1 + (n - df[term] + 0.5) / (df[term] + 0.5))
            score += idf * (tf[term] * (k1 + 1)) / (tf[term] + k1 * (1 - b + b * dl / max(avgdl, 1e-9)))
        hits.append(Hit(d.doc_id, score, "lexical"))
    return sorted(hits, key=lambda x: x.score, reverse=True)[:k]


def embed(text: str, dims: int = 64) -> list[float]:
    v = [0.0] * dims
    for token in tokenize(text):
        h = hash(token) % dims
        v[h] += 1.0
    norm = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / norm for x in v]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def dense(docs: list[Doc], query: str, k: int = 5) -> list[Hit]:
    q = embed(query)
    hits = [Hit(d.doc_id, cosine(q, embed(d.text)), "dense") for d in docs]
    return sorted(hits, key=lambda x: x.score, reverse=True)[:k]


def rrf(*ranked_lists: Iterable[Hit], k: int = 60, limit: int = 5) -> list[Hit]:
    scores: dict[str, float] = {}
    for ranked in ranked_lists:
        for rank, hit in enumerate(ranked, start=1):
            scores[hit.doc_id] = scores.get(hit.doc_id, 0.0) + 1.0 / (k + rank)
    return [Hit(doc_id, score, "rrf") for doc_id, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]]


def filter_metadata(hits: Iterable[Hit], docs: list[Doc], required: dict[str, str]) -> list[Hit]:
    allowed = {d.doc_id for d in docs if all(d.metadata.get(k) == v for k, v in required.items())}
    return [h for h in hits if h.doc_id in allowed]


def rerank(hits: Iterable[Hit], docs: list[Doc], query: str, limit: int = 5) -> list[Hit]:
    q = set(tokenize(query))
    by_id = {d.doc_id: d for d in docs}
    rescored = []
    for h in hits:
        tokens = tokenize(by_id[h.doc_id].text)
        overlap = len(q.intersection(tokens)) / max(len(q), 1)
        rescored.append(Hit(h.doc_id, 0.7 * overlap + 0.3 * h.score, "reranked"))
    return sorted(rescored, key=lambda x: x.score, reverse=True)[:limit]


def recall_at_k(ranked: Iterable[Hit], relevant: set[str], k: int) -> float:
    ids = {h.doc_id for h in list(ranked)[:k]}
    return len(ids & relevant) / max(len(relevant), 1)


def mrr(ranked: Iterable[Hit], relevant: set[str]) -> float:
    for i, h in enumerate(ranked, start=1):
        if h.doc_id in relevant:
            return 1.0 / i
    return 0.0
