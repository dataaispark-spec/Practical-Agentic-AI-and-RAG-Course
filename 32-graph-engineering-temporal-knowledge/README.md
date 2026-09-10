# Module 32 — Graph Engineering & Temporal Knowledge

**Canonical implementation:** `32-graph-engineering-temporal-knowledge/`

**Course position:** Graph Engineering Track — Module 32 of 43

**Previous:** Module 31 — Knowledge Engineering & Graph RAG  
**Next:** Module 33 — Agentic Knowledge Graph Construction

> **Core thesis:** A production knowledge graph must represent not only what is believed, but when it was true, when it was learned, where it came from, which schema produced it and whether competing claims remain unresolved.

## 1. Why this module exists

A graph that stores only `A --OWNS--> B` cannot answer historical questions safely. Enterprise knowledge changes continuously and corrections often arrive late.

```text
SOURCE
  ↓
CLAIM + PROVENANCE
  ↓
IDENTITY + SCHEMA
  ↓
VALID TIME + TRANSACTION TIME
  ↓
VALIDATION
  ├── active
  ├── superseded
  ├── contradicted
  └── quarantined
  ↓
VERSIONED GRAPH
```

## 2. Learning outcomes

You will be able to:

1. distinguish valid time, observation time, ingestion time and transaction time;
2. model temporal relationships and historical queries;
3. detect overlapping validity intervals;
4. implement supersession without deleting historical evidence;
5. distinguish contradiction from normal replacement;
6. engineer entity merge/split lifecycle;
7. evolve graph schemas with migration and rollback plans;
8. enforce provenance, tenant and ACL invariants;
9. detect graph anomalies, cycles and high-degree traversal explosions;
10. build graph-health and freshness metrics;
11. design versioned graph storage and query APIs;
12. defend a production temporal-knowledge architecture in an interview.

## 3. Core architecture

```text
                    EVIDENCE LEDGER
                           |
                           v
                 EXTRACT / RESOLVE
                           |
                           v
              SCHEMA + IDENTITY VALIDATOR
                           |
             +-------------+-------------+
             |             |             |
          temporal     provenance     access
             |             |             |
             +-------------+-------------+
                           v
                   VERSIONED CLAIMS
                    /       |       \
                   v        v        v
              active    superseded  conflict
                   \        |        /
                    +-------+-------+
                            v
                     GRAPH INDEXES
                            |
                     bounded query
                            |
                    evidence + paths
```

## 4. Component deep dive

| Component | Purpose | Typical failure |
|---|---|---|
| Evidence ledger | immutable source identity | unverifiable updates |
| Entity registry | stable IDs/aliases | false merges |
| Temporal model | valid/transaction time | historical errors |
| Schema registry | versioned ontology | migration drift |
| Validator | invariants | invalid edges |
| Supersession manager | replace without erasing | stale knowledge |
| Contradiction index | preserve disagreement | silent last-write-wins |
| Access layer | tenant/ACL scope | data leakage |
| Traversal planner | bounded paths | query explosion |
| Health evaluator | graph quality | silent degradation |

## 5. Theory / deep dive

Read [`theory/GRAPH-ENGINEERING-TEMPORAL-THEORY.md`](theory/GRAPH-ENGINEERING-TEMPORAL-THEORY.md).

Key subjects:

- temporal knowledge and bitemporal thinking;
- supersession versus contradiction;
- entity merge/split lifecycle;
- ontology/schema evolution;
- provenance as an invariant;
- domain validation;
- graph storage/index design;
- bounded traversal and cycles;
- production graph health and migration safety.

## 6. Hands-on labs

1. **BUILD** a versioned ontology and schema registry.
2. **BUILD** typed temporal entities and relations.
3. **TRY** historical queries using validity windows.
4. **TRY** late-arriving corrections.
5. **BREAK** with overlapping validity intervals.
6. **BREAK** with stale edges returned to current queries.
7. **BREAK** with duplicate identity and false merge.
8. **BREAK** with cross-tenant edge/ACL drift.
9. **BREAK** with graph cycles and high-degree hubs.
10. **MEASURE** freshness, provenance and contradiction metrics.
11. **IMPROVE** traversal using relation/time bounds.
12. **DEFEND** schema migration and rollback.

## 7. Domain-specific exercises

### Cybersecurity
Model changing `Asset → Vulnerability → Control` relationships. Query which controls were valid on the date of an incident.

### Banking
Model account ownership and policy validity across regulatory versions. Prove which policy applied to a transaction date.

### Healthcare
Model medication/guideline relationships with effective dates. Preserve old guidance for audit while preventing it from appearing as current advice.

### Manufacturing
Track machine component substitutions and maintenance intervals. Detect overlapping ownership of a component slot.

### Enterprise IT
Track service dependencies over releases. Answer: “What dependency graph existed during the outage?”

## 8. Failure-first engineering

Inject late corrections, conflicting sources, expired edges, missing timestamps, schema changes, duplicate IDs, cycles and tenant violations.

For every failure record:

**detection → evidence → containment → correction → regression test → residual risk**.

## 9. Metrics

- entity-resolution precision;
- false merge/split rate;
- provenance coverage;
- temporal-overlap rate;
- stale-edge rate;
- contradiction rate;
- orphan rate;
- traversal nodes/query;
- p50/p95 query latency;
- migration failure rate;
- tenant-isolation failure count.

## 10. Coding challenges

1. Implement interval-overlap detection.
2. Add bitemporal query semantics.
3. Implement supersession with history preservation.
4. Add contradiction indexing.
5. Build schema-version migration checks.
6. Add property tests for tenant isolation and temporal invariants.

## 11. System design challenge

Design a temporal knowledge platform for **100M entities and 1B relationships** with daily updates and late corrections. Defend storage, indexing, partitioning, temporal queries, schema migration, consistency, audit, backup and disaster recovery.

## 12. Interview bank

### Advanced
- Why are valid time and transaction time different?
- How is contradiction different from supersession?
- Why is last-write-wins unsafe for knowledge?
- How do you bound graph traversal?

### Senior/Staff
- Design bitemporal GraphRAG for regulatory history.
- How would you migrate an ontology with billions of edges?
- How do you detect graph quality degradation before users report it?

## 13. GitHub deliverables

```text
32-graph-engineering-temporal-knowledge/
├── README.md
├── EXERCISES.md
├── theory/GRAPH-ENGINEERING-TEMPORAL-THEORY.md
├── app/
├── notebooks/module_32_graph_engineering_temporal_knowledge.ipynb
└── tests/
```

## 14. Mastery gate

You must demonstrate temporal modeling, schema versioning, provenance, contradiction handling, bounded traversal, tenant isolation, failure injection, measurable graph health and a defendable migration/rollback design.

**Handoff:** M32 makes knowledge durable and historically correct. M33 introduces governed agentic construction of that knowledge.