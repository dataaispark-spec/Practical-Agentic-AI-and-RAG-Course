# Module 31 — Exercises, Labs & Mastery Challenges

## Rules
Use the same benchmark corpus and preserve evidence IDs. Every experiment must state the hypothesis, baseline, change, metric and conclusion.

## L1–L2 Foundations

1. Define five entities and five relations for Enterprise IT.
2. Draw the difference between evidence, claim, entity and edge.
3. Implement cosine similarity for a vector baseline.
4. Explain why `OWNS(A,B)` differs from `OWNS(B,A)`.

## L3 Build

5. Build a provenance-backed graph for Supplier → Contract → System → Team.
6. Implement deterministic entity IDs and aliases.
7. Implement bounded BFS with `max_hops` and `max_nodes`.
8. Return evidence paths instead of only destination entities.
9. Add tenant filtering before traversal.

## L4 Debug

10. Reverse one relation and diagnose a wrong multi-hop answer.
11. Create two aliases for the same supplier and measure false-merge impact.
12. Remove provenance from one edge and design the correct rejection behavior.
13. Create a high-degree hub and prove traversal remains bounded.

## L5 Optimize

14. Compare graph-only and vector-only Recall@5.
15. Add graph-aware features to ranking.
16. Measure latency as hop depth increases.
17. Reduce traversal work without reducing multi-hop accuracy.

## L6 Production

18. Design GraphRAG for 10M documents and 1M entities.
19. Design tenant-aware graph partitioning.
20. Define graph-health SLOs and alerts.
21. Write an ADR: “GraphRAG vs vector RAG for this workload”.

## L7 Unfamiliar problem

22. You inherit a graph with 15% duplicate entities and no reliable provenance. Design a recovery plan that improves quality without deleting evidence.

## Domain challenge cards

### SOC investigation
Build `Alert → Asset → Vulnerability → Control → Owner`. Answer an incident question with a path and source evidence.

### Banking fraud
Build `Customer → Account → Transaction → Merchant → Case → Policy`. Enforce customer/tenant scope and distinguish evidence from hypothesis.

### Healthcare knowledge
Build `Patient → Encounter → Medication → Diagnosis → Guideline`. Design privacy filtering and provenance-required clinical claims.

### Manufacturing reliability
Build `Machine → Component → FailureMode → WorkOrder → Technician`. Find an indirect maintenance dependency.

### Enterprise IT
Build `Service → Dependency → Incident → Team → Runbook`. Explain an outage using two-hop and three-hop evidence.

## Failure injection checklist

- duplicate entity;
- wrong edge direction;
- missing provenance;
- stale edge;
- cross-tenant edge;
- poisoned relation;
- traversal depth overflow;
- candidate truncation before access filtering.

For each: detection, evidence, containment, fix and regression test.

## Mastery submission

Submit:

- ontology/schema;
- runnable notebook;
- graph implementation;
- vector baseline;
- benchmark table;
- failure report;
- security test evidence;
- architecture decision record;
- five-minute design defense.
