# Module 10 — RAG Optimization & Knowledge Platform Engineering

## Mission
Turn a working RAG pipeline into a measurable, versioned, cache-aware production knowledge platform.

## Core engineering questions
- What should be cached?
- How do we invalidate stale retrieval results?
- How do embedding/model/index versions remain compatible?
- How do we optimize latency without silently destroying Recall@K?
- How do we handle document updates, deletes and re-indexing?
- How do we control context size and cost?

## Architecture
```text
Sources → ingestion → normalized docs → chunk/version registry
                                      ↓
                              embedding pipeline
                                      ↓
                            vector + lexical indexes
                                      ↓
Query → query cache → retrieval → rerank → context budget → LLM
                    ↓
              evaluation + telemetry
```

## Optimization dimensions
### Retrieval
Tune chunk size, overlap, K, filters, hybrid weights/RRF parameters and reranker depth.

### Caching
Distinguish:
- exact response cache;
- semantic query cache;
- retrieval-result cache;
- embedding cache;
- document-processing cache.

Each has different invalidation and correctness risks.

### Versioning
Every evidence object should be traceable to:
`source_id + document_version + chunk_id + embedding_version + index_version + retrieval_config_version`.

### Index lifecycle
Support build → validate → shadow → canary → promote → rollback. Never replace a production index blindly.

## Detailed labs
### Lab 1 — Baseline benchmark
Build a 100-query benchmark. Record Recall@5, MRR, p95 retrieval latency, context tokens and cost proxy.

### Lab 2 — Parameter sweep
Sweep chunk size, overlap and K. Produce a Pareto table of quality vs latency vs tokens.

### Lab 3 — Cache engineering
Implement an LRU retrieval cache. Measure hit rate and latency. Then modify one document and demonstrate stale-cache risk.

### Lab 4 — Versioned indexes
Build two index versions with different embedding dimensions/configuration. Route queries explicitly by version and prevent accidental mixing.

### Lab 5 — Incremental ingestion
Add/update/delete documents. Prove that deleted content cannot remain retrievable after the configured consistency boundary.

### Lab 6 — Context budget
Implement a token budget that selects evidence by relevance while preserving diversity and provenance.

### Lab 7 — Shadow deployment
Run old and new retrieval configurations against the same queries. Compare offline metrics before promotion.

### Lab 8 — Failure injection
Inject stale cache, mixed index versions, oversized context, duplicate chunks, failed embedding jobs and partial indexing.

## Exercises
1. Determine whether semantic caching is safe for a regulated knowledge base.
2. Design cache keys that include tenant and security context.
3. Explain why cache invalidation is a correctness problem, not merely a performance problem.
4. Design an index migration with zero-downtime rollback.
5. Find the cheapest configuration that remains within a chosen Recall@5 threshold.
6. Create a regression test for document deletion.
7. Compare pre-computed vs on-demand embeddings.
8. Design backpressure for an ingestion spike.
9. Calculate storage growth as corpus size and embedding dimension change.
10. Build a retrieval SLO and error budget.

## Production observability
Track:
- ingestion freshness;
- indexing lag;
- cache hit ratio;
- Recall@K;
- MRR/nDCG;
- retrieval p50/p95/p99;
- embedding latency;
- reranker latency;
- context tokens;
- cost/request;
- stale-result incidents;
- index-version mismatches.

## Security
Cache keys must include tenant, authorization context and relevant policy version. Never serve a cached result generated for one principal to another principal merely because the text query matches.

Deletes and revocations must propagate to every relevant cache and index. Treat stale data as a security issue when permissions or sensitive content changed.

## Interview questions
1. What should be cached in RAG?
2. Why is semantic caching risky?
3. How do you invalidate retrieval caches?
4. How do you version embeddings?
5. How do you migrate a vector index?
6. What is shadow indexing?
7. How do you guarantee delete propagation?
8. How do you optimize context size?
9. How do you choose K?
10. How do you optimize p95 without sacrificing Recall?
11. How do you design a RAG SLO?
12. How do you prevent cross-tenant cache leakage?

## System-design challenge
Design a multi-tenant knowledge platform serving 1,000 tenants, 50 million chunks and 1,000 QPS with strict tenant isolation, continuous ingestion and rollback-safe index upgrades.

## Mastery gate
You pass when you can benchmark, optimize, cache, version, migrate, invalidate and rollback a RAG system while proving that quality and security have not regressed.

## Google Colab requirement
Create `notebooks/module_10_rag_optimization.ipynb` with self-contained synthetic data and exercises for parameter sweeps, caching, versioning, context budgets and regression evaluation.
