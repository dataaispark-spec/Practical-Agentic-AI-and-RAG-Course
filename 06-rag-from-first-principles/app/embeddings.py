import hashlib
import math


def embed(text: str, dimensions: int = 128) -> list[float]:
    """Deterministic toy embedding for offline labs; not a production embedding model."""
    if dimensions < 8:
        raise ValueError("dimensions must be >= 8")
    vector = [0.0] * dimensions
    tokens = text.lower().split()
    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        for offset in (0, 4, 8):
            index = int.from_bytes(digest[offset:offset + 4], "big") % dimensions
            sign = 1.0 if digest[offset + 1] % 2 else -1.0
            vector[index] += sign
    norm = math.sqrt(sum(value * value for value in vector))
    return [value / norm for value in vector] if norm else vector


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("vectors must have equal dimensions")
    denominator = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return sum(x * y for x, y in zip(a, b)) / denominator if denominator else 0.0
