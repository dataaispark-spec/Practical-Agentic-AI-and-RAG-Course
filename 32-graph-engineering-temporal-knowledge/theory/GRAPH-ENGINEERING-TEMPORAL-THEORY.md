# Module 32 — Graph Engineering & Temporal Knowledge: Theory

## 1. Mission

Module 32 answers the production question: **How do we keep a knowledge graph correct when the world changes?**

A graph that records only current-looking edges is insufficient for enterprise reasoning. Relationships have validity intervals, source authority, schema versions, corrections, contradictions and tenant visibility.

```text
             CURRENT KNOWLEDGE
                    |
       +------------+-------------+
       |            |             |
    identity      time       provenance
       |            |             |
       +------------+-------------+
                    v
             versioned claims
                    |
       +------------+-------------+
       |            |             |
 supersession  contradiction   audit
       |            |             |
       +------------+-------------+
                    v
             queryable graph
```

## 2. Temporal knowledge model

A relationship should distinguish at least:

- observation time: when the source reported it;
- valid-from: when the fact became true;
- valid-to: when it stopped being true;
- ingestion time: when the platform received it;
- transaction/version time: when the graph changed.

These timestamps answer different questions. Do not collapse them into one `created_at` field.

Example:

```text
Supplier A --OWNS--> System X
valid: 2025-01-01 .. 2025-06-30
source: contract-v3

Supplier A --OWNS--> System Y
valid: 2025-07-01 .. present
source: contract-v4
```

A historical query for March must not return the July relationship merely because it is newer.

## 3. Bitemporal thinking

For advanced learners, distinguish **valid time** from **transaction time**.

```text
valid time:     what was true in the world?
transaction:    what did our system believe, and when?
```

This is essential when a correction arrives late. A source may say that an ownership change happened in January, but the platform learned it in March.

## 4. Supersession and contradiction

Do not use last-write-wins for knowledge claims.

```text
CLAIM A: policy timeout = 30s
source S1, valid until 2026-03-01
             |
             +---- superseded by ---->
CLAIM B: policy timeout = 60s
source S2, valid from 2026-03-01
```

Contradiction is different from supersession. Two sources may disagree for the same validity interval. Preserve both claims and route them through an explicit resolution policy.

Resolution signals may include source authority, recency, scope, corroboration and human review. The graph must retain the losing evidence rather than silently deleting it.

## 5. Entity lifecycle

Entities evolve too:

```text
DISCOVERED → RESOLVED → ACTIVE
      |          |          |
      |          |       DEPRECATED
      |          |
      +------> MERGE / SPLIT REVIEW
```

A merge requires provenance and a reversible mapping. A split is required when one identity was incorrectly conflated.

## 6. Schema evolution

Graph schemas are APIs. Changes need versions and migration rules.

Teach:

- additive changes;
- relation renames;
- relation deprecation;
- cardinality changes;
- enum expansion;
- backfill strategy;
- dual-read/dual-write migration;
- rollback plan.

Example:

```text
v1: EMPLOYEE --REPORTS_TO--> MANAGER
v2: PERSON --REPORTS_TO--> PERSON
```

A migration should specify how old edges are interpreted and how queries remain compatible during rollout.

## 7. Provenance as a graph invariant

For every active claim ask:

```text
claim → source → passage/record → timestamp → authority → tenant
```

An edge without provenance should be rejected or quarantined. Confidence without provenance is decoration, not evidence.

## 8. Graph validation

Validation should operate at several levels:

1. syntax/schema validation;
2. identity validation;
3. tenant/ACL validation;
4. temporal consistency;
5. provenance validation;
6. domain constraints;
7. contradiction detection;
8. graph-level anomaly checks.

Examples of domain constraints:

- a contract cannot end before it starts;
- a resource cannot have two exclusive owners in the same validity interval;
- a person cannot report to themselves;
- a tenant cannot reference another tenant's entity.

## 9. Bounded traversal and cycles

Graph traversal is a query planner problem, not merely a BFS exercise.

Controls:

- maximum hops;
- maximum nodes/edges;
- relation allow-list;
- tenant/ACL filters;
- time window;
- cycle detection;
- wall-clock budget;
- result-size budget.

Traversal should stop when the marginal evidence no longer justifies the operational cost.

## 10. Graph indexes and storage choices

Teach the role of adjacency indexes, entity-key indexes, temporal indexes and vector indexes. Compare:

- property graph stores;
- relational graph representations;
- RDF/triple stores;
- document stores with explicit edges.

The architectural question is not “Which graph database is best?” but “Which storage semantics match our access patterns, consistency requirements, operational skills and scale?”

## 11. Graph quality metrics

| Metric | Interpretation |
|---|---|
| entity resolution precision | identity quality |
| false merge rate | dangerous conflation |
| provenance coverage | evidence completeness |
| temporal overlap rate | validity defects |
| stale-edge rate | freshness health |
| contradiction rate | unresolved disagreement |
| orphan rate | disconnected knowledge |
| cycle/anomaly rate | structural defects |
| traversal nodes/query | query work |
| p95 query latency | service performance |
| migration error rate | schema safety |

## 12. Failure labs

Inject:

- late-arriving corrections;
- overlapping validity windows;
- missing valid-to dates;
- duplicate IDs;
- merge/split mistakes;
- cross-tenant edges;
- deprecated relation types;
- poisoned source evidence;
- traversal cycles;
- high-degree hub explosion.

The learner must diagnose the defect from observable evidence and produce a regression test.

## 13. Production architecture

```text
Sources
  |
  v
Evidence ledger -----> quarantine
  |
  v
Extractor / resolver
  |
  v
Temporal + schema validator
  |
  +---- contradiction index
  +---- provenance index
  +---- graph health metrics
  |
  v
Versioned graph store
  |
  v
Bounded query planner
  |
  v
ACL/tenant/freshness filter
  |
  v
Graph evidence → M34 hybrid retrieval
```

## 14. Handoff to Module 33

Module 32 makes the graph safe to maintain. Module 33 adds an agentic construction pipeline that proposes new entities and relations while keeping extraction, validation, approval and commit boundaries explicit.
