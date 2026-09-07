from .index import VectorIndex
from .models import RetrievalResult


class Retriever:
    def __init__(self, index: VectorIndex) -> None:
        self.index = index

    def search(self, query: str, top_k: int = 5, metadata_filter: dict[str, object] | None = None) -> list[RetrievalResult]:
        return self.index.search(query, top_k, metadata_filter)
