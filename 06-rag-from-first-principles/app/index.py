from .embeddings import cosine_similarity, embed
from .models import Chunk, RetrievalResult


class VectorIndex:
    def __init__(self) -> None:
        self._items: list[tuple[Chunk, list[float]]] = []

    def add(self, chunk: Chunk) -> None:
        self._items.append((chunk, embed(chunk.text)))

    def search(self, query: str, top_k: int = 5, metadata_filter: dict[str, object] | None = None) -> list[RetrievalResult]:
        if top_k < 1:
            raise ValueError("top_k must be >= 1")
        results: list[RetrievalResult] = []
        query_vector = embed(query)
        for chunk, vector in self._items:
            if metadata_filter and any(chunk.metadata.get(k) != v for k, v in metadata_filter.items()):
                continue
            results.append(RetrievalResult(chunk, cosine_similarity(query_vector, vector)))
        results.sort(key=lambda result: result.score, reverse=True)
        return results[:top_k]
