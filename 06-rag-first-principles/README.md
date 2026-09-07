# Module 6 — RAG From First Principles

## Mission
Build RAG without hiding the mechanism behind a framework. The learner implements ingestion, chunking, embeddings, vector search, evidence selection, context construction, grounded generation, and abstention, then measures where retrieval fails.

## Architecture

```text
Documents -> Parse -> Normalize -> Chunk -> Embed -> Index
                                               |
User question -> Query embed -> Retrieve -> Rank evidence
                                               |
                                      Context construction
                                               |
                                           Generator
                                               |
                                  Answer / Cite / Abstain
```

## Learning outcomes

- Explain RAG as a runtime knowledge architecture.
- Implement chunking and metadata propagation.
- Implement cosine similarity and top-K retrieval from scratch.
- Understand embedding geometry and its limitations.
- Separate retrieval quality from generation quality.
- Build evidence-aware prompts and abstention.
- Diagnose stale, irrelevant, duplicate, missing, and unauthorized evidence.
- Measure Recall@K, MRR, context precision, groundedness, latency, and cost.
- Explain why vector similarity is not authorization and not truth.

## 1. RAG mental model

RAG does not teach the model new facts. It supplies selected evidence at inference time.

```text
Knowledge source
      |
      v
retrieval system ----> selected evidence ----> model context
                                                   |
                                                   v
                                                answer
```

The production contract is: **retrieve the right evidence, preserve its provenance, apply access controls, and make the model use that evidence rather than inventing unsupported claims.**

## 2. Chunking

Chunking is an information-retrieval decision, not just a token-counting exercise.

Record at least:

- document_id
- chunk_id
- source
- version
- tenant_id
- section/title
- effective_at
- text
- character/token offsets

Compare fixed-size, sentence, paragraph, heading-aware, and overlap strategies.

## 3. Embeddings

An embedding maps text to a vector:

```text
text -> encoder -> [x1, x2, ... xn]
```

Similarity can be measured with cosine similarity:

```text
cos(a,b) = (a · b) / (||a|| ||b||)
```

A useful educational implementation uses deterministic hashed features so learners can inspect the entire pipeline. Production systems should replace this with a validated embedding model and benchmark it on domain data.

## 4. Retrieval

Baseline algorithm:

```text
query
  |
embed
  |
compare against indexed vectors
  |
sort by similarity
  |
top K
```

Always preserve metadata with the retrieved text.

### Retrieval filters

Apply tenant, authorization, document status, effective-date, language, and product/domain filters **before or as part of retrieval**, depending on the datastore architecture. Never rely on the LLM to enforce entitlement.

## 5. Evidence contract

Each evidence item should carry:

```json
{
  "chunk_id": "policy-17#chunk-04",
  "document_id": "policy-17",
  "version": "2026-04",
  "source": "approved-policy-store",
  "score": 0.82,
  "text": "..."
}
```

This enables citations, debugging, stale-document detection, and auditability.

## 6. Grounded generation

A grounded answer should distinguish:

- supported claims
- unsupported claims
- uncertainty
- missing evidence

A strong default is to abstain when retrieval confidence/evidence coverage is insufficient.

## 7. Evaluation

Evaluate each layer independently:

| Layer | Metrics |
|---|---|
| Chunking | boundary quality, retrieval hit rate |
| Retrieval | Recall@K, Precision@K, MRR |
| Context | relevance, redundancy, coverage |
| Generation | groundedness, correctness, citation validity |
| End-to-end | task success |
| Operations | p95 latency, cost, errors |

## 8. Failure lab

### Wrong chunk size
Symptoms: answers miss surrounding conditions or retrieve noisy context.

### Semantic mismatch
Symptoms: keyword-relevant documents are not semantically retrieved.

### Top-K overload
Symptoms: context contains many weak chunks and the answer becomes less focused.

### Stale evidence
Symptoms: older policy wins over the effective version.

### Cross-tenant retrieval
Symptoms: technically relevant evidence violates authorization.

### Retrieval-success / generation-failure
Symptoms: correct evidence exists in context but the answer ignores it.

### Retrieval-failure / generation-success illusion
Symptoms: answer sounds plausible despite missing evidence. This is a dangerous false positive.

## 9. Hands-on labs

### Lab A — Build the index
Implement:

```text
DocumentStore
Chunker
Embedder
VectorIndex
Retriever
```

### Lab B — Inspect nearest neighbors
For 20 test queries, print the top five chunks, similarity scores, and metadata. Explain every false positive.

### Lab C — Add abstention
Define a minimum evidence policy and compare unsupported-answer rate before and after.

### Lab D — Benchmark K
Run K in `{1, 3, 5, 10}` and report retrieval recall, context size, latency, and answer success.

## 10. Production design

```text
Ingestion
  -> parsing
  -> classification
  -> chunking
  -> embedding
  -> versioned index

Query
  -> identity
  -> authorization filter
  -> query transformation
  -> retrieval
  -> reranking
  -> evidence policy
  -> generation
  -> citation validation
  -> telemetry
```

## 11. Security

Threats include prompt injection inside documents, malicious metadata, tenant leakage, poisoned content, sensitive-data retrieval, and citation spoofing.

Treat retrieved text as **untrusted data**, not instructions.

## 12. Interview bank

1. Why use RAG instead of fine-tuning?
2. What makes a good chunk?
3. What is cosine similarity?
4. Why can high Recall@K still produce a bad answer?
5. How do you select K?
6. What is hybrid retrieval?
7. Why preserve document versions?
8. Where should tenant filtering happen?
9. How do you handle deleted documents?
10. How do you evaluate RAG without judging only final text?
11. What causes retrieval false positives?
12. How do you detect stale evidence?
13. How do you handle no-answer queries?
14. How do you reduce context bloat?
15. How would you scale an index to hundreds of millions of chunks?

## System-design challenge

Design a multi-tenant enterprise RAG service for 100 million chunks, with document versions, ACLs, p95 query latency under a stated target, citations, deletion propagation, and evaluation regression gates.

## Mastery gate

You can advance only after you can explain and implement every stage from document to grounded answer, show retrieval metrics, diagnose at least three retrieval failures, and demonstrate that an unauthorized chunk can never reach the model context.

## Gold challenge

Create a benchmark with at least 100 questions containing direct hits, paraphrases, distractors, stale documents, adversarial documents, and no-answer cases. Produce a report showing Recall@K, MRR, groundedness, abstention rate, latency, and cost trade-offs.
