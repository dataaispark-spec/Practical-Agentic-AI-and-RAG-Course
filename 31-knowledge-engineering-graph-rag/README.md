# Module 31 — Knowledge Engineering & Graph RAG

**Canonical implementation:** `31-knowledge-engineering-graph-rag/`

**Course position:** Graph Engineering Track — Module 31 of 43

**Previous:** Module 30 — Enterprise Agentic RAG Capstone  
**Next:** Module 32 — Graph Engineering & Temporal Knowledge

> **Core thesis:** RAG retrieves passages; knowledge engineering makes entities, claims, relationships and evidence explicit enough to inspect, traverse, validate and measure.

## 1. Why this module exists

Traditional RAG is often optimized around semantic similarity. That works well for “find passages related to X”, but becomes fragile when a task requires identity, relationships, constraints and multi-hop evidence.

Module 31 introduces the graph mental model without assuming that graphs are always superior.

```text
RAW SOURCES
 docs | APIs | tickets | tables
          |
          v
 Evidence + provenance
          |
          v
 Entities + claims + relations
          |
          v
 Validated knowledge graph
       /          \
      v            v
 graph retrieval  vector retrieval
      \            /
       +----v-----+
            |
       evidence set
            |
        RAG/Agent
```

## 2. Learning outcomes

By the end of M31 you can:

1. explain when graph structure adds value over vector retrieval;
2. design a small ontology with typed entities and directed relations;
3. model entities, claims, evidence, provenance, confidence and tenant scope;
4. resolve aliases and prevent silent duplicate/false merges;
5. implement bounded neighborhood traversal and multi-hop path retrieval;
6. distinguish evidence from generated prose and graph-derived claims;
7. compare vector-only, graph-only and hybrid retrieval;
8. measure Recall@K, MRR, multi-hop accuracy, groundedness, latency, traversal work and cost;
9. diagnose graph failures such as wrong direction, stale evidence, poisoning and traversal explosion;
10. design a production GraphRAG architecture with external authorization and verification.

## 3. Concept map

```text
Evidence
  ↓
Entity identity → Ontology → Relations → Claims
  ↓                 ↓             ↓
Provenance       constraints   temporal hooks
  \_________________+________________/
                    ↓
             Knowledge graph
                    ↓
        bounded graph retrieval
                    ↓
         graph + vector evidence
                    ↓
             rerank / verify
                    ↓
                 answer
```

## 4. Core components

| Component | Responsibility | Failure prevented |
|---|---|---|
| Evidence registry | source identity, hash, timestamp, tenant | unverifiable facts |
| Entity model | stable identity and attributes | duplicate/ambiguous entities |
| Ontology | allowed types/relations | semantic drift |
| Claim model | atomic assertion + provenance | unsupported prose |
| Graph store | queryable relationships | disconnected knowledge |
| Traversal planner | bounded paths | graph explosion |
| Access filter | tenant/ACL scope | data leakage |
| Evidence assembler | returns path + source evidence | hallucinated connections |
| Evaluator | quality/latency/cost metrics | unmeasured architecture |

## 5. Theory / deep dive

Read [`theory/KNOWLEDGE-ENGINEERING-GRAPHRAG-THEORY.md`](theory/KNOWLEDGE-ENGINEERING-GRAPHRAG-THEORY.md).

It covers:

- evidence → entity → claim → relation layers;
- ontology engineering and schema discipline;
- entity resolution and false merges;
- relation direction and semantics;
- local/global/hybrid GraphRAG;
- bounded traversal and cycle controls;
- multi-hop evidence assembly;
- graph-vs-vector decision science;
- graph health metrics;
- security and tenant isolation;
- production architecture and Module 32 handoff.

## 6. Hands-on progression

### Lab 1 — BUILD: ontology
Define a minimal enterprise ontology for **Supplier → Contract → System → Team**.

### Lab 2 — BUILD: graph
Create deterministic entities, claims and provenance-backed edges.

### Lab 3 — TRY: neighborhood retrieval
Implement depth-limited traversal and inspect returned paths.

### Lab 4 — TRY: multi-hop question
Answer a question requiring two or three validated relationships.

### Lab 5 — TRY: vector baseline
Use the same corpus to establish a semantic retrieval baseline.

### Lab 6 — BREAK: entity duplication
Create aliases and a false merge; measure the impact on retrieval.

### Lab 7 — BREAK: relation direction
Reverse one edge and diagnose the wrong multi-hop answer.

### Lab 8 — BREAK: provenance
Attempt to activate an edge with missing source evidence.

### Lab 9 — BREAK: traversal explosion
Attempt an excessive hop/node budget and prove the guard triggers.

### Lab 10 — BREAK: tenant leakage
Insert an edge crossing tenants and demonstrate rejection.

### Lab 11 — BREAK: graph poisoning
Inject a fabricated relationship and verify it cannot become trusted evidence.

### Lab 12 — MEASURE: retrieval benchmark
Compare vector-only, graph-only and hybrid retrieval using the same questions.

### Lab 13 — IMPROVE: path-aware ranking
Add relation/path/freshness signals and measure whether quality improves.

### Lab 14 — DEFEND: evidence report
Generate an answer with explicit entity IDs, edge IDs, source references and confidence.

## 7. Domain-specific tracks

### Cybersecurity
`Asset → Vulnerability → CVE → Exploit → Control → Owner`

Exercise: identify an affected asset and prove the vulnerability path without crossing tenant boundaries.

### Banking
`Customer → Account → Transaction → Merchant → Case → Policy`

Exercise: build a fraud-investigation graph and distinguish evidence from analyst hypotheses.

### Healthcare
`Patient → Encounter → Medication → Diagnosis → Guideline`

Exercise: retrieve a treatment-policy path while enforcing privacy scope and source provenance.

### Manufacturing
`Machine → Component → FailureMode → MaintenanceAction → Technician`

Exercise: find an indirect dependency explaining a recurring equipment failure.

### Enterprise IT
`Service → Dependency → API → Team → Incident → Runbook`

Exercise: trace an outage from service to owning team through dependency relationships.

## 8. Failure contract

For every injected defect record:

**symptom → evidence → hypothesis → experiment → root cause → fix → regression test → residual risk**

## 9. Measurements

Minimum scorecard:

- entity resolution precision;
- provenance coverage;
- Recall@K;
- MRR;
- multi-hop path accuracy;
- groundedness/provenance coverage;
- nodes/edges traversed;
- p50/p95 latency;
- tokens and cost per verified task;
- tenant-isolation failures.

## 10. Exercises

See [`EXERCISES.md`](EXERCISES.md) for progressive L1–L7 tasks, domain variants, coding challenges, debugging scenarios and system-design work.

## 11. System-design challenge

Design GraphRAG for **10M enterprise documents** across multiple tenants. Explain ingestion, ontology governance, entity resolution, graph/vector indexes, bounded traversal, authorization, freshness, evaluation, caching, cost and disaster recovery.

## 12. Interview bank

### Core
- When is GraphRAG better than vector RAG?
- Why is entity resolution a retrieval problem?
- What makes an edge trustworthy?
- Why must traversal be bounded?

### Senior
- Design multi-hop retrieval over 100M entities.
- How do you prevent graph poisoning?
- How would you diagnose a graph retrieval regression?
- Why can hybrid retrieval reduce quality despite higher recall?

### Staff/Architect
- What evidence would justify the operational cost of a graph?
- How do you evolve ontology and retrieval without breaking production?

## 13. GitHub deliverables

```text
31-knowledge-engineering-graph-rag/
├── README.md
├── EXERCISES.md
├── theory/
│   └── KNOWLEDGE-ENGINEERING-GRAPHRAG-THEORY.md
├── app/
├── notebooks/
│   └── module_31_knowledge_engineering_graph_rag.ipynb
└── tests/
```

## 14. Mastery gate

Pass only when you can:

**Know** the graph/RAG trade-off → **Construct** a validated graph → **Connect** multi-hop evidence → **Measure** retrieval and cost → **Break** graph assumptions → **Defend** tenant/provenance controls → **Explain** the architecture decision.

Required evidence: BUILD + TRY + BREAK + MEASURE + IMPROVE + DEFEND plus a reproducible vector-vs-graph-vs-hybrid experiment.

**Handoff:** M31 introduces explicit knowledge. M32 makes it temporal, versioned and production-maintainable.