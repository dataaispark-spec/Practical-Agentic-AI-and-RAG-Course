# Module 7 — Embeddings + Vector Databases

## Mission
Move from a toy vector index to production-grade vector retrieval engineering. The learner compares embedding models, similarity functions, exact search and approximate nearest-neighbor (ANN) indexes, metadata filtering, indexing lifecycle, recall/latency trade-offs, and vector-database architecture.

## Learning outcomes

By completion, you can:

1. Explain what embeddings represent and what they do not represent.
2. Select an embedding model using domain-specific evaluation rather than model popularity.
3. Normalize vectors and reason about cosine, dot-product, and Euclidean distance.
4. Implement exact nearest-neighbor search.
5. Explain ANN structures such as HNSW and IVF at engineering level.
6. Measure Recall@K against latency and memory.
7. Design metadata filtering and tenant isolation.
8. Handle embedding version changes and re-indexing.
9. Detect embedding drift and retrieval regressions.
10. Choose between managed vector DB, relational vector extension, search engine, and custom index.

## 1. Embeddings are representations, not truth

```text
Text / image / code
        |
        v
   embedding model
        |
        v
   dense vector
        |
        v
similarity / retrieval
```

An embedding compresses information into a representation useful for a particular model and objective. Similarity is therefore model-dependent. A high similarity score does not mean two documents are factually equivalent, authorized, current, or safe.

## 2. Similarity mathematics

For vectors `a` and `b`:

```text
cosine(a,b) = a·b / (||a|| ||b||)
```

For normalized vectors, dot product and cosine similarity become equivalent.

Euclidean distance:

```text
sqrt(sum((ai-bi)^2))
```

Understand which metric the index expects; using the wrong metric can silently damage retrieval quality.

## 3. Exact search baseline

The gold-standard baseline is exhaustive comparison:

```text
query vector
    |
    +---- compare with vector 1
    +---- compare with vector 2
    +---- ...
    +---- compare with vector N
    |
    v
sort / top K
```

It is expensive at large N but invaluable as a correctness reference for ANN benchmarking.

## 4. ANN engineering

At scale, exact search may be too slow or expensive. ANN methods trade a small amount of recall for large performance gains.

### HNSW

Conceptually, HNSW creates navigable graph layers. Search explores promising neighbors rather than every vector.

Engineering knobs commonly include:

- graph construction connectivity
- search-time exploration depth
- vector dimensionality
- index memory
- build time

### IVF

Inverted-file approaches partition vector space into clusters and search selected partitions.

Trade-offs include:

```text
more partitions searched -> higher recall / higher latency
fewer partitions searched -> lower latency / potentially lower recall
```

Do not memorize knob names; learn the underlying recall/latency trade-off.

## 5. Benchmark methodology

Always compare ANN against an exact-search ground truth set.

For each query:

```text
exact top K
      |
      +---- compare with ANN top K
      |
      v
Recall@K
```

Record:

- Recall@1/5/10
- p50/p95/p99 latency
- QPS
- index build time
- memory footprint
- storage footprint
- filtering latency

## 6. Metadata filtering

A production vector record should typically contain:

```json
{
  "id": "doc-7#chunk-12",
  "vector": "...",
  "tenant_id": "tenant-a",
  "document_type": "policy",
  "version": "2026-07",
  "effective_at": "2026-07-01",
  "classification": "internal"
}
```

Filtering is not optional decoration. It is part of retrieval correctness and security.

### Critical distinction

```text
Similarity relevance != authorization
```

A perfectly relevant chunk must still be excluded if the requester cannot access it.

## 7. Embedding model selection

Evaluate candidate models on:

- domain retrieval benchmark
- multilingual coverage if required
- query/document asymmetry
- vector dimensionality
- throughput
- price
- latency
- licensing/deployment constraints
- privacy/data residency

The best general-purpose embedding model is not necessarily the best model for a specific enterprise corpus.

## 8. Embedding versioning

Never silently replace an embedding model while leaving old vectors indistinguishable.

Use explicit metadata:

```text
embedding_model = model-x
embedding_version = 3
index_version = 2026-09-07
```

A migration can follow:

```text
old index
   |
   +---- continue serving
   |
new embedding model
   |
re-embed
   |
validate against benchmark
   |
shadow / canary
   |
switch alias
   |
retire old index
```

## 9. Vector-database choices

| Architecture | Strength | Watch-out |
|---|---|---|
| In-process index | simple, cheap, educational | limited scale/durability |
| Relational DB + vector extension | joins + transactional data | vector scale/feature trade-offs |
| Search engine | mature filtering + lexical search | operational complexity |
| Managed vector DB | scaling and specialized retrieval | cost/vendor dependence |
| Custom ANN | maximum control | high engineering burden |

Choose based on workload, operational maturity, security, consistency, and cost—not benchmark marketing alone.

## 10. Failure lab

### Failure 1 — High-dimensional cost explosion
Increasing vector dimensions improves one benchmark but causes memory and latency growth.

### Failure 2 — Wrong similarity metric
A normalized-vector assumption is violated and ranking quality silently drops.

### Failure 3 — ANN recall regression
An ANN index becomes fast but misses critical evidence.

### Failure 4 — Filter-after-retrieval bug
Top-K is selected globally and unauthorized/irrelevant candidates are removed afterward, leaving too little valid evidence.

### Failure 5 — Embedding migration mismatch
Queries use model B while documents remain embedded with model A.

### Failure 6 — Tenant leakage
A missing filter exposes another tenant's chunk.

## 11. Hands-on labs

### Lab A — Exact-search baseline
Generate vectors for a labelled dataset and compute exact top-K.

### Lab B — ANN simulation
Implement or configure an ANN index and measure recall against exact search.

### Lab C — Metadata filtering
Benchmark retrieval with tenant, document-type, version, and date filters.

### Lab D — Model bake-off
Compare at least two embedding models on the same dataset and report:

```text
Recall@K
MRR
p95 latency
throughput
vector dimension
estimated cost
memory
```

### Lab E — Migration
Create v1 and v2 indexes, shadow traffic, compare rankings, then perform a controlled cutover.

## 12. Production architecture

```text
                 +------------------+
                 | Embedding Model  |
                 +--------+---------+
                          |
                    versioned vectors
                          |
                    +-----v------+
                    | Vector DB   |
                    +-----+------+
                          |
              +-----------+-----------+
              | filters / ACL / scope |
              +-----------+-----------+
                          |
                       top-K
                          |
                      reranker
                          |
                       evidence
```

Use an alias/version strategy so index migrations do not require application code changes.

## 13. Observability

Track:

- query count
- empty-result rate
- Recall@K on evaluation traffic
- p50/p95/p99 latency
- filter selectivity
- candidate count
- index version
- embedding version
- cache hit rate
- error rate
- memory utilization

A sudden drop in average similarity can be a useful signal, but never treat it as a complete quality metric.

## 14. Security

Threats include:

- cross-tenant retrieval
- malicious documents
- embedding/index poisoning
- sensitive metadata exposure
- stale access-control state
- accidental logging of vectors or source content

Use defense in depth: identity, policy, datastore filters, result validation, audit logs, and regression tests.

## 15. Interview bank

1. What is an embedding?
2. Why normalize vectors?
3. Compare cosine and dot product.
4. What is ANN?
5. Why benchmark ANN against exact search?
6. Explain HNSW conceptually.
7. Explain IVF conceptually.
8. What is Recall@K?
9. How do you choose K?
10. What causes vector-index recall regression?
11. How do you migrate embedding models safely?
12. How do you enforce tenant isolation?
13. When would you choose a relational vector extension?
14. How do vector dimensions affect cost?
15. How would you debug a sudden retrieval-quality drop?
16. How would you operate billions of vectors?
17. What does index freshness mean?
18. How do deletes propagate?
19. What should be logged for vector retrieval?
20. Design a highly available vector-search tier.

## System-design challenge

Design a vector retrieval service serving 10,000 queries/second, with 500 million chunks, tenant isolation, metadata filtering, index versioning, online migration, p99 latency targets, and a Recall@10 regression gate.

## Mastery gate

You advance only when you can produce an exact-search ground truth, benchmark an ANN index against it, explain every major recall/latency trade-off, enforce tenant filtering, and complete a versioned embedding migration without mixing incompatible vectors.

## Gold challenge

Build a reproducible benchmark that sweeps:

```text
embedding model × similarity metric × K × ANN search parameters × filter selectivity
```

and outputs a Pareto-style decision table for quality, latency, memory, and cost.
