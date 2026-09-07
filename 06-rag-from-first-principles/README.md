# Module 6 — RAG From First Principles

## Mission
Build retrieval-augmented generation without hiding the important mechanics behind a framework. You will implement a small RAG engine from raw text through chunking, vector representation, similarity search, evidence selection, prompt assembly, and grounded answer generation.

## Learning outcomes

You will be able to:

1. Explain why parametric model knowledge is insufficient for changing/private information.
2. Design chunking and metadata strategies.
3. Understand embeddings as vectors rather than magic search tokens.
4. Implement similarity search from first principles.
5. Separate retrieval quality from generation quality.
6. Inspect retrieved evidence and diagnose failures.
7. Add citations and abstention behavior.
8. Measure Recall@K, MRR, latency and cost.
9. Explain when RAG is worse than long context or a deterministic database query.
10. Design a production RAG architecture with authorization and observability.

## The RAG pipeline

```text
Documents
   |
   v
Normalize / parse
   |
   v
Chunk + metadata
   |
   v
Embedding
   |
   v
Vector index
   |
   v
Query embedding
   |
   v
Similarity search
   |
   v
Top-K evidence
   |
   v
Prompt/context assembly
   |
   v
LLM
   |
   v
Grounded answer + citations / abstention
```

## 1. What RAG actually solves

RAG is a runtime knowledge architecture. It does not magically make a model truthful.

The model still generates the answer; retrieval supplies evidence that the application can inspect and constrain.

Use RAG when information is:

- private
- current or frequently changing
- too large to place into every prompt
- naturally represented as searchable documents

Do not use RAG merely because a project is called an AI assistant. A deterministic database query is usually preferable for exact transactional facts.

## 2. First-principles vector search

Represent a document chunk as a vector:

```text
chunk -> [0.12, -0.44, 0.91, ...]
```

Represent the query similarly:

```text
query -> [0.08, -0.40, 0.87, ...]
```

A common similarity measure is cosine similarity:

```text
cos(q, d) = (q · d) / (||q|| ||d||)
```

The implementation is simple enough to build with Python/NumPy. The hard production problems are usually elsewhere: ingestion quality, chunk boundaries, metadata filtering, authorization, freshness, ranking, evaluation and operations.

## 3. Chunking is information architecture

Bad chunking can destroy retrieval before the model ever sees the data.

Compare:

```text
Document
  -> arbitrary 500-character slices
```

with:

```text
Document
  -> section
      -> subsection
          -> coherent chunk
              + document_id
              + version
              + tenant
              + source
              + effective_date
```

Start with structure-aware chunks when possible. Use overlap only when it addresses a real boundary problem; excessive overlap increases index size and duplicate evidence.

## 4. Metadata is part of retrieval

A production chunk should carry enough metadata for filtering and citation:

```json
{
  "chunk_id": "policy-42-v3-c07",
  "document_id": "policy-42",
  "version": "3",
  "tenant_id": "tenant-a",
  "source": "hr-policy.pdf",
  "section": "Leave",
  "effective_date": "2026-07-01"
}
```

Important: **retrieval correctness is not authorization**. Authorization should be enforced before or during retrieval using deterministic identity and entitlement controls.

## 5. Minimal RAG engine

Build these components without a framework:

```text
Document
Chunker
EmbeddingModel
VectorIndex
Retriever
ContextBuilder
Generator
RAGPipeline
```

Recommended interface:

```python
class Retriever(Protocol):
    def search(self, query: str, top_k: int = 5) -> list[Chunk]: ...
```

The first implementation may use deterministic toy embeddings so the tests do not depend on an external provider.

## 6. Retrieval vs generation

Keep the stages observable:

```text
Query
 |
 +--> retrieved chunks
 |
 +--> ranking scores
 |
 +--> selected evidence
 |
 +--> generated answer
```

If the answer is wrong, ask first:

1. Was the right evidence retrieved?
2. Was it ranked highly enough?
3. Was it actually passed to the model?
4. Did the model use the evidence correctly?

Without these boundaries, teams often “fix the prompt” for a retrieval problem.

## 7. Grounding and abstention

A robust RAG application should support:

```text
Evidence sufficient?
   |
   +-- yes --> answer using evidence
   |
   +-- no --> abstain / request clarification / route elsewhere
```

Do not manufacture confidence when evidence is missing.

For high-risk domains, require citations or evidence IDs and validate that cited evidence belongs to the authorized retrieval set.

## 8. Evaluation

### Retrieval metrics

**Recall@K:** whether a known relevant document/chunk appears in the top K.

**MRR:** how high the first relevant result appears.

Example:

```text
Query Q1 -> relevant chunk ranked #1 -> reciprocal rank 1.0
Query Q2 -> relevant chunk ranked #4 -> reciprocal rank 0.25
```

### Generation metrics

Evaluate separately:

- groundedness / faithfulness
- answer correctness
- citation correctness
- abstention correctness
- task success

Then add operational metrics:

- retrieval latency
- generation latency
- p95/p99 latency
- token usage
- cost/task

## 9. Hands-on lab — NumPy RAG Engine

Create:

```text
06-rag-from-first-principles/
├── app/
│   ├── models.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── index.py
│   ├── retriever.py
│   ├── prompt.py
│   └── pipeline.py
├── datasets/
│   ├── documents.jsonl
│   └── queries.jsonl
├── tests/
│   ├── test_chunker.py
│   ├── test_index.py
│   └── test_retrieval.py
└── docs/
    └── FAILURE-LAB.md
```

### Build order

1. Define document/chunk contracts.
2. Implement structure-aware chunking.
3. Add deterministic toy embeddings.
4. Implement cosine similarity.
5. Build top-K index search.
6. Add metadata filters.
7. Create retrieval evaluation cases.
8. Add a context builder.
9. Add a fake generator.
10. Inspect every retrieval trace.

## 10. Failure lab

### Failure A — Giant chunks

**Symptom:** relevant information exists but retrieval returns broad, noisy passages.

**Experiment:** compare chunk sizes while holding the embedding model and dataset constant.

### Failure B — Tiny chunks

**Symptom:** retrieved fragments lack the context required to answer.

**Fix:** structure-aware boundaries and measured overlap.

### Failure C — Semantic miss

**Symptom:** keyword-equivalent queries retrieve unrelated chunks.

**Fix path:** inspect embeddings, add hybrid retrieval in Module 9, and create representative query variants.

### Failure D — Stale information

**Symptom:** old policy wins over current policy.

**Fix:** metadata filters/version awareness and freshness tests.

### Failure E — Cross-tenant retrieval

**Symptom:** retrieval finds a relevant chunk belonging to another tenant.

**Lesson:** tenant authorization must be deterministic and testable.

### Failure F — Correct retrieval, wrong answer

**Symptom:** evidence is clearly relevant but the answer contradicts it.

**Diagnosis:** generation/grounding failure, not necessarily retrieval failure.

## 11. Production architecture

```text
                Identity / Policy
                       |
                       v
User -> Query -> Retrieval Gateway
                    |
          +---------+---------+
          |                   |
      metadata filter     vector search
          |                   |
          +---------+---------+
                    |
                    v
               rerank/evidence
                    |
                    v
              Context Builder
                    |
                    v
                  Model
                    |
          +---------+---------+
          |                   |
       validator          citations
          |                   |
          +---------+---------+
                    v
                 Answer
```

For large systems, the vector index becomes an infrastructure service, but the conceptual boundaries remain the same.

## 12. Architecture trade-offs

| Choice | Advantage | Risk |
|---|---|---|
| Long context | simple pipeline | context cost/noise |
| Vector retrieval | scalable semantic search | embedding/retrieval errors |
| Keyword retrieval | exact terminology | weaker semantic matching |
| Hybrid retrieval | complementary signals | more tuning |
| RAG | current/private evidence | ingestion + retrieval complexity |
| Fine-tuning | behavior/style adaptation | poor fit for frequently changing facts |

## 13. Interview bank

1. Explain RAG from first principles.
2. Why does chunking matter?
3. What is cosine similarity?
4. What is Recall@K?
5. What is MRR?
6. Why can high Recall@K still yield bad answers?
7. When would you choose a database query instead of RAG?
8. How do you handle document versioning?
9. How do you enforce tenant isolation?
10. How do you prevent stale chunks from winning?
11. How do you decide chunk size?
12. What is hybrid retrieval?
13. Why can overlap increase cost without improving quality?
14. How do you diagnose retrieval vs generation failure?
15. How would you evaluate citations?
16. How would you implement abstention?
17. How do you handle a 50-million-document corpus?
18. What metadata belongs on a chunk?
19. How would you reduce RAG latency?
20. Design a multi-tenant enterprise RAG system.

## Mastery gate

You can advance when you can build a working RAG pipeline from raw documents to top-K evidence, explain every retrieval score, measure retrieval quality, detect stale/unauthorized evidence, and demonstrate why a failure belongs to ingestion, retrieval, context assembly, or generation.

### Gold challenge

Given 100 documents and 30 labeled questions:

- achieve measurable Recall@5
- produce evidence IDs for every answer
- abstain when evidence is insufficient
- enforce tenant filters
- benchmark at least three chunking strategies
- report latency and cost
- create five deliberate failure cases and diagnose each one.
