# Module 33 — Agentic Knowledge Graph Construction

**Canonical implementation:** `33-agentic-knowledge-graph-construction/`

**Course position:** Graph Engineering Track — Module 33 of 43

**Previous:** Module 32 — Graph Engineering & Temporal Knowledge  
**Next:** Module 34 — Graph + Vector Hybrid Retrieval

> **Core thesis:** Agents can accelerate knowledge construction, but model-generated knowledge must remain a proposal until provenance, schema, identity, temporal, security and domain gates approve it.

## 1. Why this module exists

Manual graph curation does not scale, but unrestricted LLM write access is unsafe. Module 33 engineers the middle ground:

```text
messy source
    ↓
agentic extraction
    ↓
entity resolution
    ↓
relation proposals
    ↓
validation + provenance + policy
    ├── reject
    ├── quarantine
    └── approve
             ↓
       idempotent commit
             ↓
        monitor / evaluate
             ↓
          rollback
```

## 2. Learning outcomes

By the end you can:

1. build structured entity/relation extraction;
2. separate model confidence from source authority;
3. resolve entities with reversible decisions;
4. validate relation schema, provenance, tenant and temporal constraints;
5. detect contradictions before promotion;
6. route high-risk knowledge to human approval;
7. bind approval to exact proposal content/version;
8. perform idempotent graph writes;
9. monitor extraction and promotion quality;
10. roll back unsafe graph mutations without deleting history;
11. defend the constructor against prompt injection and poisoning;
12. design agentic KG construction for enterprise scale.

## 3. Architecture

```text
                    SOURCES
          docs / tickets / APIs / tables
                       |
                       v
                +--------------+
                | Agent        |
                | extractor    |
                +------+-------+
                       |
                  proposals
                       |
                       v
             +---------------------+
             | Resolver / Validator|
             | schema | identity   |
             | provenance | time   |
             | tenant | domain      |
             +----------+----------+
                        |
          +-------------+-------------+
          |             |             |
        reject      quarantine     approval
                                      |
                                      v
                              commit gateway
                                      |
                              versioned graph
                                      |
                              health evaluator
                                      |
                                  rollback
```

## 4. Component responsibilities

| Component | Responsibility | Failure if absent |
|---|---|---|
| Extractor | candidate facts | manual bottleneck |
| Resolver | entity identity | duplicate/false merges |
| Schema validator | legal predicates/types | semantic drift |
| Provenance validator | evidence traceability | fabricated facts |
| Temporal validator | validity windows | historical corruption |
| Policy gate | risk/tenant/approval | unauthorized promotion |
| Commit gateway | idempotent mutation | duplicates |
| Contradiction detector | conflict visibility | silent false knowledge |
| Health evaluator | quality metrics | unmeasured degradation |
| Rollback manager | safe reversal | persistent bad state |

## 5. Theory / deep dive

Read [`theory/AGENTIC-KG-CONSTRUCTION-THEORY.md`](theory/AGENTIC-KG-CONSTRUCTION-THEORY.md).

It covers extraction strategies, entity resolution, confidence versus authority, validation layers, human approval, idempotent writes, contradiction handling, rollback, security and evaluation.

## 6. Hands-on labs

1. **BUILD:** deterministic candidate extractor.
2. **BUILD:** typed proposal schema.
3. **TRY:** entity resolution with aliases.
4. **TRY:** provenance-backed relation proposal.
5. **BREAK:** unsupported predicate.
6. **BREAK:** unknown entity.
7. **BREAK:** fabricated citation.
8. **BREAK:** cross-tenant proposal.
9. **BREAK:** contradictory policy.
10. **BREAK:** duplicate delivery after timeout.
11. **BREAK:** prompt injection inside source text.
12. **MEASURE:** extraction precision/recall.
13. **MEASURE:** promotion precision and quarantine rate.
14. **IMPROVE:** add authority-aware validation.
15. **DEFEND:** rollback and audit evidence.

## 7. Domain-specific tracks

### Cybersecurity
Extract `CVE → Product → Version → Asset → Control` from advisories and tickets. Exercise: reject an LLM-invented vulnerable version unless source evidence supports it.

### Banking
Extract `Customer → Account → Transaction → Case → Policy`. Exercise: require approval before promoting a relation that changes a fraud-risk classification.

### Healthcare
Extract `Drug → Condition → Guideline → Evidence`. Exercise: quarantine unsupported clinical claims and preserve citation spans.

### Manufacturing
Extract `Machine → Component → FailureMode → WorkOrder`. Exercise: detect contradictory maintenance instructions before commit.

### Enterprise IT
Extract `Service → Dependency → Incident → Owner → Runbook`. Exercise: update the dependency graph from an incident while preventing prompt injection from ticket text.

## 8. Failure contract

Every injected fault must produce:

**observable → evidence → hypothesis → experiment → root cause → containment → fix → regression assertion**.

## 9. Measurements

- entity precision/recall/F1;
- relation precision/recall/F1;
- unsupported-claim rate;
- provenance coverage;
- false merge rate;
- contradiction-detection precision;
- promotion precision;
- quarantine rate;
- duplicate-write rate;
- rollback success;
- downstream retrieval/task success.

## 10. Coding challenges

1. Implement canonical proposal hashing.
2. Add schema and relation allow-lists.
3. Build a reversible entity merge registry.
4. Implement contradiction indexing.
5. Add approval-bound proposal hashes.
6. Add idempotent commit/reconciliation.
7. Build rollback with immutable audit events.
8. Add property tests for tenant isolation.

## 11. System design challenge

Design an agentic KG builder processing **1M source updates/day**. Explain extraction routing, batching, model selection, confidence calibration, human-review queues, schema versions, graph writes, rollback, evaluation, cost and disaster recovery.

## 12. Interview bank

### Advanced
- Why is model confidence not equivalent to truth?
- Why must approval bind to exact proposal content?
- How do you handle contradictory extracted facts?

### Senior/Staff
- Design a zero-trust graph write pipeline.
- How would you safely scale LLM extraction to billions of documents?
- How do you detect silent degradation in extraction quality?

## 13. GitHub deliverables

```text
33-agentic-knowledge-graph-construction/
├── README.md
├── EXERCISES.md
├── theory/AGENTIC-KG-CONSTRUCTION-THEORY.md
├── app/
├── notebooks/module_33_agentic_knowledge_graph_construction.ipynb
└── tests/
```

## 14. Mastery gate

Demonstrate extraction, identity resolution, provenance, validation, contradiction handling, approval, idempotent commit, rollback, security failure injection and measurable downstream benefit.

**Handoff:** M33 governs graph construction. M34 determines how graph and vector evidence should work together for retrieval.