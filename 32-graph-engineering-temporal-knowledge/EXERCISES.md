# Module 32 — Exercises, Labs & Mastery Challenges

## L1–L2 Foundations

1. Define valid time, transaction time, observation time and ingestion time.
2. Draw a temporal edge lifecycle.
3. Explain supersession versus contradiction.
4. Identify three graph invariants for your domain.

## L3 Build

5. Implement temporal edges with `valid_from` and `valid_to`.
6. Implement interval-overlap detection.
7. Add provenance and authority metadata.
8. Add tenant and ACL validation.
9. Implement historical queries.

## L4 Debug

10. Inject an overlapping validity interval and locate the defect.
11. Deliver a late correction and preserve the old evidence.
12. Create a false entity merge and design a reversible split.
13. Query current state and accidentally return a stale edge; diagnose it.
14. Create a traversal cycle and prove the query terminates.

## L5 Optimize

15. Add temporal indexes to reduce candidate scans.
16. Compare traversal cost at hop depths 1–5.
17. Add freshness-aware ranking.
18. Measure query latency before and after graph partitioning.

## L6 Production

19. Design schema migration v1 → v2 for 100M relationships.
20. Define a bitemporal audit model for regulatory evidence.
21. Design backup/restore and rollback semantics.
22. Define graph-health SLOs and alerts.

## L7 Unfamiliar problem

23. A regulator asks what your organization believed about a supplier on a past date, even though the authoritative source arrived months later. Design the query and evidence model.

## Domain challenge cards

### Cybersecurity
Reconstruct the control graph as it existed on an incident date.

### Banking
Prove which policy version governed a transaction at execution time.

### Healthcare
Prevent expired guidance from appearing as current while retaining historical audit evidence.

### Manufacturing
Detect overlapping machine-component ownership intervals.

### Enterprise IT
Reconstruct the dependency graph during an outage window.

## Failure injection

- late-arriving correction;
- overlapping validity;
- missing timestamp;
- duplicate identity;
- false merge;
- cross-tenant relation;
- deprecated schema relation;
- traversal cycle;
- high-degree hub.

## Mastery submission

Submit schema versions, temporal model, migration plan, historical-query examples, failure report, graph-health scorecard, security tests and rollback evidence.
