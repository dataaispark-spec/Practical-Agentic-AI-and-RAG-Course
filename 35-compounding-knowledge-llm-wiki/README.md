# Module 35 — Karpathy-style Compounding Knowledge / LLM Wiki

> **Position:** M31–M34 teach knowledge/graph construction and retrieval; **M35 teaches how validated evidence becomes maintained, compounding organizational knowledge**; M36 then teaches the execution loop that operates over persistent state.

This is **Karpathy-inspired compounding knowledge**, not a claim of an official Karpathy methodology.

## Why this module matters

Raw RAG answers questions. A compounding knowledge system maintains a durable evidence-backed knowledge layer: new evidence is compared with existing claims, validated, merged or superseded, contradiction is made visible, pages are recompiled, and bad updates can be rolled back.

The central rule is:

**Evidence is authoritative input; claims are normalized knowledge; wiki pages are compiled views. Generated prose is never evidence by itself.**

## Learning outcomes

By the end of M35, learners can:

1. explain why append-only RAG context does not create compounding organizational knowledge;
2. design an evidence → claim → validation → promotion → compilation lifecycle;
3. model provenance, confidence, freshness, temporal validity and version history;
4. resolve duplicate entities without silent merges;
5. detect and preserve contradictions instead of using last-write-wins;
6. compile bounded, cited wiki pages and agent context;
7. measure provenance coverage, freshness, contradiction, duplicate rate and context size;
8. defend the knowledge layer against poisoning, prompt injection and cross-tenant leakage;
9. roll back bad updates while retaining audit history;
10. benchmark raw RAG vs curated wiki vs KG vs KG+vector hybrid.

## Core architecture

```text
RAW SOURCES
 docs | APIs | tickets | policies | observations
                     |
                     v
             +----------------+
             | Evidence       |
             | Registry       |
             +-------+--------+
                     |
                     v
             +----------------+
             | Claim / Entity |
             | Extraction     |
             +-------+--------+
                     |
                     v
             +-------------------------+
             | Validation / Governance |
             | provenance | authority  |
             | schema | tenant | time   |
             +----+---------------+----+
                  |               |
               reject           accept
                  v               v
            QUARANTINE      KNOWLEDGE STORE
                                  |
             +--------------------+------------------+
             |                    |                  |
             v                    v                  v
        active claims       entity/topic pages   change history
             |                    |                  |
             +--------------------+------------------+
                                  v
                         CONTEXT COMPILER
                         bounded + cited
                                  |
                                  v
                         RAG / GRAPH / AGENT
                                  |
                                  v
                           EVALUATION LOOP
                                  |
                                  +----> next update
```

## Components — what each one protects

| Component | Purpose | Failure if missing |
|---|---|---|
| Evidence Registry | immutable source identity/hash/tenant/time | citations cannot be reconstructed |
| Claim Model | atomic normalized assertions | prose becomes ambiguous knowledge |
| Entity Resolver | stable identity and aliases | duplicate concepts proliferate |
| Validator | quality, provenance and policy gate | poisoned claims become active |
| Contradiction Detector | explicit conflict representation | stale/false knowledge silently wins |
| Knowledge Store | active + historical versions | updates destroy history |
| Page Compiler | deterministic human-readable projection | wiki drifts from claims |
| Context Compiler | bounded evidence-backed agent context | context bloat / false authority |
| Change Log | mutation audit trail | operators cannot explain changes |
| Health Evaluator | measurable quality | “knowledge quality” becomes opinion |
| Rollback Manager | safe reversal | bad updates remain active |

## Theory / deep dive

Read **[`theory/COMPOUNDING-KNOWLEDGE-THEORY.md`](theory/COMPOUNDING-KNOWLEDGE-THEORY.md)** before the implementation lab. It covers:

- evidence vs claims vs compiled pages;
- claim lifecycle and state transitions;
- provenance vs authority;
- contradiction handling;
- temporal validity and freshness;
- entity resolution and duplicate concepts;
- context compilation and boundedness;
- security and tenant isolation;
- health/evaluation metrics;
- rollback and audit semantics;
- relationship to M31–M36.

## Mechanism: the knowledge lifecycle

```text
DISCOVERED → NORMALIZED → VALIDATED → ACTIVE
                         |             |
                         v             v
                     QUARANTINED   SUPERSEDED

ACTIVE → CONTRADICTED → REVIEW → ACTIVE / SUPERSEDED
ACTIVE → ROLLED_BACK → prior valid state
```

The implementation in `app/wiki.py` is intentionally deterministic and framework-free. It provides evidence registration, provenance-aware claims, validation, supersession, quarantine, bounded context compilation, health metrics and rollback.

## Practical labs

### Lab 1 — BUILD: evidence registry
Create source records with tenant, content hash, observation time and authority metadata.

### Lab 2 — BUILD: atomic claims
Represent one assertion per claim and attach explicit evidence.

### Lab 3 — TRY: incremental compounding
Insert a first claim, then add new evidence that supersedes it. Inspect active state and history.

### Lab 4 — TRY: entity/duplicate resolution
Create aliases and near-duplicate concepts; define an explicit merge decision instead of silently combining them.

### Lab 5 — BREAK: append-only knowledge
Append contradictory/stale information and observe why retrieval quality and trust degrade.

### Lab 6 — BREAK: provenance loss
Attempt to activate a claim without registered evidence. The system must reject it.

### Lab 7 — BREAK: poisoned knowledge
Inject suspicious claims and route them to quarantine rather than active knowledge.

### Lab 8 — BREAK: tenant boundary
Attempt to reference evidence belonging to another tenant. The promotion must be denied.

### Lab 9 — BREAK: contradiction
Represent conflicting claims and design a source-authority/temporal/human-review policy.

### Lab 10 — MEASURE: knowledge health
Measure provenance coverage, freshness SLA, contradiction rate, duplicate rate, promotion quality, rollback success and context size.

### Lab 11 — MEASURE: benchmark
Hold corpus/questions/evaluator constant and compare raw document RAG, curated wiki, KG and KG+vector hybrid.

### Lab 12 — IMPROVE: bounded context
Reduce context size while preserving task success and provenance coverage.

### Lab 13 — DEFEND: recovery
Perform a bad promotion, audit it, roll it back, and prove the historical record remains intact.

## Failure-first engineering

| Failure | Required diagnosis | Corrective principle |
|---|---|---|
| stale claim remains active | missing temporal/supersession logic | explicit lifecycle |
| citation disappeared | claim not tied to evidence | provenance is mandatory |
| duplicate concepts | weak identity resolution | stable entity identity |
| contradiction hidden | last-write-wins | conflict as first-class state |
| poisoned claim promoted | missing gate | quarantine + validation |
| context explodes | page used as unbounded memory | bounded compiler |
| generated summary treated as source | authority confusion | evidence/claim/page separation |
| bad update persists | no reversible mutation | versioning + rollback |

## Measurements

Minimum lab scorecard:

| Metric | Question |
|---|---|
| Provenance coverage | Can every active claim be traced to evidence? |
| Freshness SLA | How much active knowledge is within policy? |
| Contradiction rate | How much active knowledge is conflicted? |
| Duplicate rate | How many identities remain unresolved? |
| Promotion precision | How many accepted claims are actually correct? |
| Rollback success | Can a bad update be safely reversed? |
| Context size | How much evidence reaches the agent? |
| Task success | Does curated knowledge improve the target task? |
| Update latency | How quickly can validated evidence compound? |
| Review load | How much human intervention is required? |

## Security

Treat the knowledge layer as a security boundary. Defend against source poisoning, fabricated citations, prompt injection in documents, unauthorized promotion, cross-tenant references, stale authoritative sources and rollback abuse.

Minimum controls: tenant isolation, immutable evidence identity, provenance-required promotion, policy gates, quarantine, bounded context, append-only audit events, least-privilege mutation and authorized rollback.

## Industry exercise

**Scenario:** An enterprise maintains security-policy knowledge across PDFs, tickets and internal APIs. Build a knowledge service that receives new evidence daily, extracts candidate claims, validates them, detects contradictions, updates topic pages, emits an audit trail and supplies bounded context to an agent.

**Acceptance criteria:**

- no active claim without traceable evidence;
- no cross-tenant evidence reference;
- stale claims are superseded rather than silently duplicated;
- contradictions are visible;
- suspicious claims are quarantined;
- rollback restores a prior valid state;
- context has a hard size bound;
- health metrics are emitted;
- raw RAG vs wiki vs KG vs hybrid comparison is reproducible.

## System-design challenge

Design a multi-tenant compounding knowledge platform for 10M documents and frequent policy changes. Explain ingestion, identity resolution, claim validation, contradiction handling, temporal versions, storage, indexing, context compilation, auditability, rollback, evaluation, cost and disaster recovery.

## Coding challenges

1. Implement a deterministic claim merge policy with provenance preservation.
2. Add an explicit contradiction index keyed by entity/topic.
3. Implement freshness scoring and stale-claim detection.
4. Add a source-authority policy with human-review escalation.
5. Build a bounded context compiler that maximizes evidence coverage under a token/character budget.
6. Add property-based tests for rollback and tenant isolation.

## Debugging challenge

A new policy is accepted, but an agent still cites the previous policy. Determine whether the defect is in evidence registration, claim supersession, page compilation, context compilation, cache invalidation or retrieval ranking. Produce a minimal failing test before changing code.

## GitHub deliverables

- `theory/COMPOUNDING-KNOWLEDGE-THEORY.md`
- `app/wiki.py`
- `tests/test_wiki.py`
- `notebooks/module_35_compounding_knowledge_llm_wiki.ipynb`
- benchmark/evaluation notes from the four-way comparison
- failure injection and rollback evidence

## Mastery gate

Pass only if you can independently explain and demonstrate:

- **Know:** why compounding knowledge differs from document RAG;
- **Construct:** evidence-backed claims and entity identity;
- **Connect:** claims, provenance, contradictions and temporal validity;
- **Compound:** validated updates and deterministic page compilation;
- **Measure:** health and benchmark metrics;
- **Defend:** poisoning and tenant-isolation controls;
- **Recover:** audited rollback without history loss;
- **Reason:** when curated wiki is better or worse than raw RAG/KG/hybrid.

### Mastery threshold

A passing submission must include executable evidence for **BUILD + TRY + BREAK + MEASURE + IMPROVE + DEFEND**, plus a short architecture rationale and a reproducible comparison experiment.
