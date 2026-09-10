# Module 34 — Exercises, Labs & Mastery Challenges

## L1–L2 Foundations

1. Explain vector versus graph retrieval signals.
2. Implement cosine similarity.
3. Implement a simple graph path search.
4. Explain why Recall@K is not sufficient for final-answer quality.

## L3 Build

5. Build vector-only retrieval.
6. Build graph-only retrieval.
7. Build candidate union.
8. Implement Reciprocal Rank Fusion.
9. Add tenant/ACL and temporal filters before truncation.
10. Build a deterministic reranker.

## L4 Debug

11. Remove a graph edge and diagnose multi-hop failure.
12. Remove a vector candidate and diagnose semantic miss.
13. Inject a poisoned subgraph.
14. Create duplicate candidates for one entity.
15. Move authorization filtering after top-k and demonstrate the defect.
16. Increase traversal depth until budget exhaustion.

## L5 Optimize

17. Compare score fusion versus RRF.
18. Tune candidate fan-out and measure recall/latency.
19. Tune reranker depth and measure quality/cost.
20. Add graph path relevance to ranking.

## L6 Production

21. Design hybrid retrieval for 100M documents + 100M entities.
22. Define p95 latency and cost budgets.
23. Build a regression benchmark with release thresholds.
24. Write an ADR deciding whether hybrid retrieval is justified.

## L7 Unfamiliar problem

25. Hybrid retrieval improves Recall@20 by 7% but doubles p95 latency and increases cost by 3×. Decide whether to ship it for an SLO-constrained workload and specify the experiment that would settle the decision.

## Domain challenge cards

### Cybersecurity
Combine advisory vectors with `Asset → Vulnerability → Control → Owner` paths.

### Banking
Combine transaction-policy passages with customer/account/case graph constraints.

### Healthcare
Combine literature retrieval with guideline relationships while preserving provenance.

### Manufacturing
Combine maintenance text with machine/component/failure-mode paths.

### Enterprise IT
Combine incident vectors with service/dependency/team graph paths.

## Benchmark table

Record for every strategy:

`Recall@K | MRR | nDCG | multi-hop accuracy | groundedness | candidates | traversal work | p50 | p95 | tokens | cost/success`

## Mastery submission

Submit all five retrieval baselines, benchmark results, failure report, security ordering proof, optimization experiment and architecture decision record.
