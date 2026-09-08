from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
import hashlib
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


def _validate_k(k: int) -> None:
    if k < 1:
        raise ValueError("k must be >= 1")


def bm25(docs: list[Doc], query: str, k: int = 5, k1: float = 1.5, b: float = 0.75) -> list[Hit]:
    _validate_k(k)
    q = tokenize(query)
    if not q or not docs:
        return []
    lengths = [len(tokenize(d.text)) for d in docs]
    avgdl = sum(lengths) / len(lengths)
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
    return sorted(hits, key=lambda x: (-x.score, x.doc_id))[:k]


def _bucket(token: str, dims: int) -> int:
    return int.from_bytes(hashlib.blake2b(token.encode(), digest_size=8).digest(), "big") % dims


def embed(text: str, dims: int = 64) -> list[float]:
    if dims <= 0:
        raise ValueError("dims must be positive")
    v = [0.0] * dims
    for token in tokenize(text):
        v[_bucket(token, dims)] += 1.0
    norm = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / norm for x in v]


def cosine(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("vectors must have equal dimensions")
    return sum(x * y for x, y in zip(a, b))


def dense(docs: list[Doc], query: str, k: int = 5) -> list[Hit]:
    _validate_k(k)
    if not docs:
        return []
    q = embed(query)
    hits = [Hit(d.doc_id, cosine(q, embed(d.text)), "dense") for d in docs]
    return sorted(hits, key=lambda x: (-x.score, x.doc_id))[:k]


def rrf(*ranked_lists: Iterable[Hit], k: int = 60, limit: int = 5) -> list[Hit]:
    if k <= 0 or limit < 1:
        return []
    scores: dict[str, float] = {}
    for ranked in ranked_lists:
        for rank, hit in enumerate(ranked, start=1):
            scores[hit.doc_id] = scores.get(hit.doc_id, 0.0) + 1.0 / (k + rank)
    return [Hit(doc_id, score, "rrf") for doc_id, score in sorted(scores.items(), key=lambda x: (-x[1], x[0]))[:limit]]


def filter_metadata(hits: Iterable[Hit], docs: list[Doc], required: dict[str, str]) -> list[Hit]:
    """Filter an already-ranked candidate list; use secure_hybrid_retrieve for pre-retrieval ACLs."""
    by_id = {d.doc_id: d for d in docs}
    return [h for h in hits if h.doc_id in by_id and all(by_id[h.doc_id].metadata.get(key) == value for key, value in required.items())]


def secure_hybrid_retrieve(docs: list[Doc], query: str, required: dict[str, str], candidate_k: int = 20, limit: int = 5) -> list[Hit]:
    """Apply deterministic metadata/tenant constraints before candidate truncation and fusion."""
    _validate_k(candidate_k)
    _validate_k(limit)
    authorized = [d for d in docs if all(d.metadata.get(key) == value for key, value in required.items())]
    lexical = bm25(authorized, query, min(candidate_k, len(authorized))) if authorized else []
    semantic = dense(authorized, query, min(candidate_k, len(authorized))) if authorized else []
    return rrf(lexical, semantic, limit=limit)


def rerank(hits: Iterable[Hit], docs: list[Doc], query: str, limit: int = 5) -> list[Hit]:
    _validate_k(limit)
    q = set(tokenize(query))
    by_id = {d.doc_id: d for d in docs}
    rescored = []
    for h in hits:
        if h.doc_id not in by_id:
            continue
        tokens = tokenize(by_id[h.doc_id].text)
        overlap = len(q.intersection(tokens)) / max(len(q), 1)
        rescored.append(Hit(h.doc_id, 0.7 * overlap + 0.3 * h.score, "reranked"))
    return sorted(rescored, key=lambda x: (-x.score, x.doc_id))[:limit]


def recall_at_k(ranked: Iterable[Hit], relevant: set[str], k: int) -> float:
    if k < 1 or not relevant:
        return 0.0
    ids = {h.doc_id for h in list(ranked)[:k]}
    return len(ids & relevant) / len(relevant)


def mrr(ranked: Iterable[Hit], relevant: set[str]) -> float:
    if not relevant:
        return 0.0
    for i, h in enumerate(ranked, start=1):
        if h.doc_id in relevant:
            return 1.0 / i
    return 0.0
