# Module 31 — GraphRAG Benchmark Protocol

Use one corpus, one labeled query set and one security policy.

Compare:
1. vector-only;
2. graph-only;
3. hybrid.

Report: Recall@1/5/10, MRR, multi-hop path accuracy, provenance coverage, nodes traversed, p50/p95 latency, context tokens and cost per verified task.

A benchmark is incomplete unless failures are stratified by semantic, entity-resolution, relationship, provenance and authorization errors.