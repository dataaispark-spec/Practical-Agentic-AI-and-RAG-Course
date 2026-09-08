# Module 34 — Graph + Vector Hybrid Retrieval

Compare retrieval strategies rather than assuming GraphRAG is superior. Build a deterministic benchmark for vector-only, graph-only, reciprocal-rank fusion and graph+vector+reranking.

## Labs
1. Build the same corpus for all strategies.
2. Implement vector similarity baseline.
3. Implement bounded graph retrieval.
4. Fuse rankings with RRF.
5. Add metadata/ACL filters before candidate truncation.
6. Add reranking.
7. Create multi-hop questions.
8. Measure Recall@K, MRR, nDCG and multi-hop accuracy.
9. Measure p50/p95 latency, traversal work and tokens.
10. Write an ADR for when hybrid retrieval is justified.

## Failure-first
Graph miss, vector miss, contradictory evidence, poisoned subgraph, candidate truncation before authorization, traversal explosion and reranker overfit.

## Production rule
Use the simplest retrieval architecture that meets quality and operational requirements.
