from app.rag import Document, VectorIndex, build_context, chunk_document, cosine, should_abstain


def test_chunking_preserves_provenance():
    doc = Document("d1", "alpha beta gamma delta", tenant_id="t1", version="v2", source="manual")
    chunks = chunk_document(doc, size=2, overlap=0)
    assert len(chunks) == 2
    assert chunks[0].tenant_id == "t1"
    assert chunks[0].version == "v2"
    assert chunks[0].chunk_id.startswith("d1#chunk-")


def test_cosine_identical_vectors_is_one():
    assert cosine([1, 0], [1, 0]) == 1.0


def test_retrieval_filters_tenant():
    index = VectorIndex()
    index.add([
        *chunk_document(Document("a", "refund policy customer payment", tenant_id="A"), 20, 0),
        *chunk_document(Document("b", "refund policy customer payment", tenant_id="B"), 20, 0),
    ])
    results = index.search("refund policy", k=10, tenant_id="A")
    assert results
    assert all(item.chunk.tenant_id == "A" for item in results)


def test_context_contains_evidence_id():
    evidence = VectorIndex()
    evidence.add(chunk_document(Document("d", "approved support procedure"), 20, 0))
    result = evidence.search("support procedure", 1)
    assert "[d#chunk-0000]" in build_context(result)


def test_abstains_without_evidence():
    assert should_abstain([])
