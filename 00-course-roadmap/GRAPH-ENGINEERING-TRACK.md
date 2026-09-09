# Graph Engineering Track — Knowledge, GraphRAG & Compounding Knowledge

**Scope:** Modules 31–35, with integration hooks into Modules 36–43  
**Status:** normative subject-matter guidance  
**Canonical branch:** `main`  
**Updated:** 2026-09-09

The general engineering rules live in [`COURSE-ENGINEERING-STANDARDS.md`](./COURSE-ENGINEERING-STANDARDS.md). This track adds graph-specific concepts, failure modes and evidence.

> **Graph engineering = extract structured knowledge, validate it, preserve provenance and time, retrieve bounded subgraphs, and use graph evidence under policy.**

## Two different graphs

```text
KNOWLEDGE GRAPH                         AGENT / TASK GRAPH
entities                                goals
actions/claims                          states
relations                               transitions
evidence                                tools/workers
provenance                              approvals
time                                    recovery
   |                                       |
   v                                       v
what the system knows                   how the system works
```

Do not confuse a knowledge graph with a workflow graph. They answer different questions and require different correctness tests.

## Module progression

| Module | Primary focus | Distinct outcome |
|---:|---|---|
| 31 | Knowledge Engineering & Graph RAG | typed knowledge model + bounded evidence retrieval |
| 32 | Graph Engineering & Temporal Knowledge | ontology/entity-resolution evolution + valid-time semantics |
| 33 | Agentic Knowledge Graph Construction | proposal → validation → promotion with provenance |
| 34 | Graph + Vector Hybrid Retrieval | reproducible vector/graph/hybrid/rerank comparison |
| 35 | Compounding Knowledge / LLM Wiki | maintained knowledge updates, contradictions, freshness and rollback |

## Knowledge lifecycle

```text
RAW SOURCES
  ↓
parse / normalize
  ↓
entity + claim + relation proposals
  ↓
entity resolution
  ↓
provenance + temporal validity
  ↓
validation / policy gate
  ↓
KNOWLEDGE GRAPH
  ├── bounded graph retrieval
  └── vector retrieval
          ↓
      hybrid retrieval
          ↓
        rerank
          ↓
        agent
          ↓
    verify / act under policy
          ↓
      validated write-back
```

Where relevant, graph records should preserve identifiers/types, `tenant_id`, `source_id`, claim/provenance references, confidence, valid-time fields, ACL and schema version.

## Graph correctness

A graph is evidence, not unrestricted truth. Learners must distinguish:

- proposed vs validated knowledge;
- source fact vs extracted claim;
- current vs historical relation;
- supported vs unsupported inference;
- duplicate entity vs same entity;
- contradiction vs supersession.

## Temporal knowledge

Teach valid-time explicitly. For example, one ownership relation can be valid through a historical interval and a replacement relation can begin later. A historical query and a current query must not silently return the same answer.

Where transaction-time semantics are introduced, keep them conceptually distinct from valid-time semantics.

## GraphRAG benchmark

Use the same query set and compare, where meaningful:

1. vector-only;
2. graph-only;
3. graph + vector;
4. graph + vector + reranker/verifier.

Measure task-relevant quality plus latency, traversal work, token/cost impact and maintenance/update cost. Explicitly report cases where adding a graph makes the system worse.

## Compounding knowledge

The course uses “Karpathy-inspired compounding knowledge” to describe the pattern of turning sources into maintained, linked, increasingly useful knowledge. It is **not** presented as an official methodology or attribution.

The target loop is:

```text
raw source
→ curated knowledge
→ entities / claims / relations / citations
→ contradiction / change detection
→ validated update
→ change log / health report
→ better future retrieval
```

Core operations should include creating/updating an entity, resolving duplicates, adding a claim, linking evidence, adding/superseding a relation, recording contradictions, validating changes, bounded-neighborhood queries, provenance inspection and rollback.

## Failure / security lab

Relevant failure classes include:

- duplicate entities and entity collisions;
- wrong relation direction;
- hallucinated claims;
- missing or forged provenance;
- temporal overlap / stale edges;
- contradictions;
- cross-tenant leakage;
- graph poisoning;
- unbounded traversal;
- cyclic or misleading inference.

```text
graph poisoning
→ false claim/edge
→ wrong retrieval
→ wrong inference
→ unsafe decision
→ unauthorized action
```

The action remains subject to identity, authorization, policy, budget, approval, verification and audit even when the graph appears highly confident.

## Vendor-neutral baseline

The educational baseline should use Python plus local/synthetic fixtures and deterministic fake extraction where useful. Graph databases and query languages are optional extensions, not prerequisites for learning the mechanism.

## Completion evidence

A graph-focused module is practice-complete when the learner can demonstrate:

1. typed schema;
2. provenance;
3. bounded retrieval;
4. entity-resolution behavior;
5. temporal/contradiction handling where relevant;
6. security/poisoning tests;
7. vector-vs-graph/hybrid evidence where applicable;
8. graph health metrics;
9. bad-update rollback/recovery;
10. an ADR explaining when a graph is unnecessary.
