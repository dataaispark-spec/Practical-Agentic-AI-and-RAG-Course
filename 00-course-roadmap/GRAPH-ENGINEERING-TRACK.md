# Graph Engineering Track — Knowledge, GraphRAG and Compounding Knowledge

The course already teaches workflow/state graphs (Module 16), agent/task graphs (Modules 19–22), retrieval (6–12), memory/provenance (15, 26, 34) and durable autonomy (33–36). The missing graph was the graph representing **what the system knows**. This track adds that layer without turning the course into a vendor-specific graph-database course.

> **Graph engineering = extract structured knowledge, validate it, preserve provenance and time, retrieve bounded subgraphs, and let agents reason over evidence under policy.**

The phrase **Karpathy-inspired compounding knowledge** means the broader pattern of turning raw sources into maintained, linked, increasingly useful knowledge. It is not presented as an official Karpathy methodology.

## Two graphs

```text
KNOWLEDGE GRAPH                         AGENT / TASK GRAPH
entities                                goals
relations                               states
claims                                  transitions
evidence                                tools
provenance                              workers
time                                    approvals
   |                                       |
   v                                       v
what the system knows                   how the system works
```

AegisAI now explicitly supports both.

## Integration into Modules 31–38

| Module | Existing focus | Graph upgrade |
|---|---|---|
| 31 | Loop Engineering | graph-aware observations, bounded traversal, knowledge-state checks |
| 32 | Harness Engineering | KG/GraphRAG as governed harness capabilities |
| 33 | Long-Running Agents | durable graph writes, temporal edges, stale-knowledge recovery |
| 34 | Skills/Memory/Continual Harnesses | compounding knowledge, skill↔knowledge links, contradictions |
| 35 | Environments/Verifiers/Agentic RL | graph tasks, multi-hop verifiers, anti-reward-hacking checks |
| 36 | Recursive Self-Improvement | self-improving extraction/retrieval with gates and rollback |
| 37 | Computer Use/Always-On | graph-grounded digital workers and evidence-backed actions |
| 38 | Frontier Capstone | graph + vector + reranker + durable harness + computer use |

No existing frontier capability is removed; graph engineering becomes a cross-cutting capability.

## Knowledge lifecycle

```text
RAW SOURCES
  -> parsing
  -> entity / claim extraction
  -> relation extraction
  -> entity resolution
  -> provenance + temporal validity
  -> validation gate
  -> KNOWLEDGE GRAPH
       |             \
   graph search     vector search
       \             /
        HYBRID RETRIEVAL
              -> rerank -> agent -> verify/act -> validated write-back
```

Minimum records expose, where applicable: `tenant_id`, entity/relation IDs and types, `source_id`, `claim_id`, confidence, `valid_from`, `valid_to`, timestamps, ACL, provenance and schema version.

## GraphRAG benchmark

Every graph retrieval lab compares the same dataset using: **vector-only**, **graph-only**, **graph+vector**, and **graph+vector+reranker+verifier**.

Measure Recall@K, MRR/nDCG, multi-hop accuracy, groundedness, citation correctness, p50/p95 latency, traversal work, tokens, cost per verified task and maintenance/update cost. Learners must document cases where GraphRAG is worse.

## Karpathy-inspired compounding knowledge

Build a deterministic pipeline in which repeated ingestion **updates knowledge rather than blindly appending documents**:

```text
raw -> curated knowledge -> entities / claims / relations / citations / contradictions
                         -> queries/inbox -> change log -> health report
```

Required operations: create entity, resolve duplicate, add claim, link evidence, add relation, supersede stale relation, record contradiction, validate, bounded-neighborhood query, generate a knowledge page, inspect provenance and rollback a bad update.

## Temporal knowledge

Teach valid-time explicitly. An acquisition edge may be valid from 2024-01-01 to 2025-06-30, followed by an ownership edge from 2025-07-01 onward. This supports historical incident reconstruction and current-policy questions.

## Graph failure/security lab

Executable failures cover duplicate entities, entity collisions, hallucinated/incorrect-direction relations, missing provenance, contradictions, stale edges, temporal overlap, tenant/ACL leakage, graph poisoning, unbounded traversal and cyclic reasoning.

```text
graph poisoning -> false claim/edge -> wrong retrieval -> wrong inference
-> wrong tool decision -> unauthorized action
```

Graph security therefore includes storage security **plus relationship integrity, provenance integrity, inference boundaries and action authorization**. The graph is evidence, never unrestricted authority.

## Vendor-neutral implementation

Core: Python + SQLite where useful + deterministic fake extraction for CI/Colab. NetworkX and Neo4j/Cypher/Gremlin/SPARQL/GraphRAG frameworks are optional extensions. The learner must understand the mechanism before the vendor.

## Completion evidence

1. typed graph schema;
2. entity/relation/claim extraction baseline;
3. entity-resolution tests;
4. provenance and temporal edges;
5. bounded graph retrieval;
6. vector-vs-graph-vs-hybrid benchmark;
7. compounding-knowledge update pipeline;
8. graph poisoning tests;
9. graph health metrics;
10. an ADR explaining when **not** to use a knowledge graph.
