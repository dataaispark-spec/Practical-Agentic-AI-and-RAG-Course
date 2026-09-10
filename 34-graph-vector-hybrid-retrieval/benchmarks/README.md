# Module 34 — Hybrid Retrieval Benchmark

Run the same corpus/query/evaluator through:

1. vector-only;
2. graph-only;
3. union;
4. RRF;
5. hybrid + reranker.

Report Recall@1/5/10, MRR, nDCG, multi-hop accuracy, groundedness, candidates, traversal work, p50/p95 latency, tokens and cost per successful task.

Decision rule: ship hybrid only when the quality gain survives security, latency, cost and maintenance constraints.