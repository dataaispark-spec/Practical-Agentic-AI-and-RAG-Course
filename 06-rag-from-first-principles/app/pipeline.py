from collections.abc import Callable
from dataclasses import dataclass

from .models import RetrievalResult
from .retriever import Retriever


@dataclass(frozen=True)
class RAGResponse:
    answer: str
    evidence: tuple[RetrievalResult, ...]
    abstained: bool


class RAGPipeline:
    def __init__(self, retriever: Retriever, generator: Callable[[str], str], min_score: float = 0.05) -> None:
        self.retriever = retriever
        self.generator = generator
        self.min_score = min_score

    def answer(self, query: str, top_k: int = 5, metadata_filter: dict[str, object] | None = None) -> RAGResponse:
        results = self.retriever.search(query, top_k, metadata_filter)
        evidence = tuple(result for result in results if result.score >= self.min_score)
        if not evidence:
            return RAGResponse("I do not have sufficient evidence to answer this question.", (), True)
        context = "\n\n".join(f"[{item.chunk.chunk_id}] {item.chunk.text}" for item in evidence)
        prompt = f"Answer only from the evidence below. Cite chunk IDs.\n\nQuestion: {query}\n\nEvidence:\n{context}"
        return RAGResponse(self.generator(prompt), evidence, False)
