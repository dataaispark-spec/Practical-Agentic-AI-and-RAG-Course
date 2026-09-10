# Graph Engineering Track — Knowledge, GraphRAG & Compounding Knowledge

**Scope:** Modules 31–35, with integration hooks into Modules 36–43  
**Status:** normative subject-matter guidance  
**Canonical branch:** `main`  
**Updated:** 2026-09-10

The general engineering rules live in [`COURSE-ENGINEERING-STANDARDS.md`](./COURSE-ENGINEERING-STANDARDS.md). This track adds graph-specific concepts, failure modes and evidence.

> **Graph engineering = extract structured knowledge, validate it, preserve provenance and time, retrieve bounded subgraphs, combine complementary retrieval signals, and use graph evidence under policy.**

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

| Module | Primary focus | Distinct engineering outcome |
|---:|---|---|
| 31 | Knowledge Engineering & Graph RAG | ontology + entities/claims + bounded graph evidence + GraphRAG decision |
| 32 | Graph Engineering & Temporal Knowledge | temporal/bitemporal semantics + schema evolution + contradiction/supersession |
| 33 | Agentic Knowledge Graph Construction | governed extraction + resolution + validation + approval + idempotent commit + rollback |
| 34 | Graph + Vector Hybrid Retrieval | vector/graph baselines + RRF + reranking + multi-hop benchmark + retrieval economics |
| 35 | Compounding Knowledge / LLM Wiki | maintained evidence-backed knowledge, context compilation and rollback |

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
VERSIONED KNOWLEDGE GRAPH
  ├── bounded graph retrieval
  └── vector retrieval
          ↓
      hybrid retrieval
          ↓
        rerank / verify
          ↓
        agent
          ↓
    validated write-back
          ↓
      compounding knowledge
```

## Module 31 — explicit knowledge and GraphRAG

Teach ontology engineering, evidence/entity/claim separation, relation direction, entity identity, bounded traversal, multi-hop paths, graph-vs-vector decision science and evidence assembly. The learner must build and benchmark graph-only, vector-only and hybrid baselines.

## Module 32 — temporal graph correctness

Teach valid time, observation time, ingestion time and transaction time; supersession versus contradiction; entity merge/split; schema versioning/migration; temporal constraints; stale-edge detection; bounded traversal and graph health.

## Module 33 — governed graph construction

Teach agentic extraction as a proposal process. The model may propose; validators, provenance checks, tenant policy, risk gates, human approval and idempotent commit decide what becomes active. Rollback is a governed mutation and never history deletion.

## Module 34 — hybrid retrieval economics

Teach candidate union, Reciprocal Rank Fusion, score fusion, graph/path signals, reranking, multi-hop datasets and retrieval error decomposition. Hold evaluation conditions constant and report quality **and** operational cost. A hybrid architecture must be justified by evidence, not fashion.

## Graph correctness invariants

Learners must distinguish:

- proposed vs validated knowledge;
- source evidence vs extracted claim;
- current vs historical relation;
- supported vs unsupported inference;
- duplicate entity vs same entity;
- contradiction vs supersession;
- graph evidence vs authorization.

## Security ordering

```text
identity / tenant
      ↓
ACL / resource scope
      ↓
temporal / freshness constraints
      ↓
graph + vector candidate generation
      ↓
fusion / reranking
      ↓
bounded evidence context
      ↓
verification
```

Never allow a graph edge, retrieved document, memory item or model-generated claim to grant permission.

## Benchmark discipline

For M31–M34, preserve a reproducible corpus/query/evaluator version and record:

`quality | provenance | safety | latency | traversal work | tokens | cost | maintenance impact`

Report negative results. If graph retrieval adds complexity but does not improve task success, the correct engineering decision may be **not to use a graph**.

## Domain transfer

Recommended shared schemas:

- Cybersecurity: `Asset → Vulnerability → Control → Owner`;
- Banking: `Customer → Account → Transaction → Case → Policy`;
- Healthcare: `Drug/Patient → Condition/Encounter → Guideline/Evidence`;
- Manufacturing: `Machine → Component → FailureMode → WorkOrder`;
- Enterprise IT: `Service → Dependency → Incident → Team → Runbook`.

Each domain should include normal cases, multi-hop cases, contradictory evidence, poisoned input and tenant/ACL tests.

## Failure / security lab

Relevant classes:

- duplicate entities and entity collisions;
- wrong relation direction;
- hallucinated claims;
- missing or forged provenance;
- temporal overlap / stale edges;
- contradictions;
- cross-tenant leakage;
- graph poisoning;
- unbounded traversal;
- candidate truncation before authorization;
- reranker regression;
- schema migration defects.

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

The educational baseline uses Python, local/synthetic fixtures and deterministic fake extraction where useful. Graph databases, Cypher, RDF/SPARQL and hosted vector stores are extension exercises rather than prerequisites for learning the mechanisms.

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
10. an ADR explaining when a graph is unnecessary;
11. a domain-specific transfer exercise;
12. executable notebook evidence following **Predict → Build → Try → Break → Debug → Measure → Improve → Defend**.
