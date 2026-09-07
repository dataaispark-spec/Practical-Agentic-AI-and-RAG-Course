import pytest

from app.chunker import chunk_document
from app.embeddings import cosine_similarity, embed
from app.index import VectorIndex
from app.models import Document
from app.retriever import Retriever


def test_chunker_preserves_document_metadata():
    chunks = chunk_document(Document("d1", "alpha beta gamma", {"tenant": "a"}), max_chars=8, overlap=2)
    assert chunks
    assert all(c.document_id == "d1" and c.metadata["tenant"] == "a" for c in chunks)


def test_embedding_is_deterministic_and_cosine_self_is_one():
    vector = embed("retrieval quality")
    assert vector == embed("retrieval quality")
    assert cosine_similarity(vector, vector) == pytest.approx(1.0)


def test_vector_index_returns_ranked_results_and_filters_metadata():
    index = VectorIndex()
    index.add(Document("d1", "python retrieval systems", {"tenant": "a"}) and __import__("app.models", fromlist=["Chunk"]).Chunk("d1-c0", "d1", "python retrieval systems", {"tenant": "a"}))
    index.add(__import__("app.models", fromlist=["Chunk"]).Chunk("d2-c0", "d2", "financial settlement", {"tenant": "b"}))
    results = index.search("python retrieval", top_k=2, metadata_filter={"tenant": "a"})
    assert len(results) == 1
    assert results[0].chunk.chunk_id == "d1-c0"


def test_retriever_delegates_to_index():
    index = VectorIndex()
    retriever = Retriever(index)
    assert retriever.search("anything") == []
