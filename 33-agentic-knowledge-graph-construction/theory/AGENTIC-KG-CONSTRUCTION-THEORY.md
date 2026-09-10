# Module 33 — Agentic Knowledge Graph Construction: Theory

## 1. Mission

Module 33 turns a knowledge graph from a manually curated artifact into a **governed construction pipeline** in which models and agents propose candidate knowledge, while deterministic validators, provenance checks, policy gates and commit controls decide what becomes active.

Core lifecycle:

```text
SOURCE
  ↓
EXTRACT
  ↓
NORMALIZE
  ↓
RESOLVE
  ↓
PROPOSE
  ↓
VALIDATE
  ↓
┌───────────────┬────────────────┐
│               │                │
REJECT       QUARANTINE       APPROVE
                                  ↓
                                COMMIT
                                  ↓
                              MONITOR
                                  ↓
                              ROLLBACK
```

## 2. Why agents are useful—and dangerous

LLMs are strong at extracting candidate entities and relations from messy language. They are weak as unconditional authorities.

The architecture must therefore separate:

- **proposal generation** — probabilistic;
- **validation** — deterministic/domain governed;
- **authorization** — external to the model;
- **commit** — controlled side effect;
- **verification** — independent evidence check.

## 3. Candidate data model

A proposal should contain:

```text
proposal_id
subject
predicate
object/value
source_id
source_span
tenant_id
confidence
extractor/model version
created_at
schema_version
risk_class
```

A proposal is not an active graph fact.

## 4. Extraction strategies

Compare:

### Rule-based extraction
High determinism; narrow coverage.

### NER + relation models
Better structure; requires model evaluation.

### LLM structured extraction
Flexible and useful for long-tail language; requires schema validation, provenance and adversarial testing.

### Agentic extraction
The agent can decide which documents, tools or follow-up sources to inspect, but the same commit controls still apply.

## 5. Entity resolution

The constructor must decide whether a candidate refers to an existing entity.

```text
candidate "Acme Corp"
      |
      +--> exact key match?
      |
      +--> alias match?
      |
      +--> contextual attributes?
      |
      +--> similarity candidate?
      |
      +--> confidence threshold
             |
        +----+----+
        |         |
      merge     review
```

Never allow an LLM to silently create an identity merge with no reversible record.

## 6. Relation validation

Validation layers:

1. schema: is the predicate allowed?
2. identity: do both entities exist?
3. provenance: is the source traceable?
4. tenant: are both endpoints in scope?
5. temporal: are validity intervals coherent?
6. domain: does the relationship violate a business invariant?
7. contradiction: does active evidence disagree?
8. risk: does this relation require human approval?

## 7. Confidence is not truth

Teach the distinction:

```text
model confidence = how strongly the model predicts the relation
source authority = how trustworthy the evidence source is
validation status = whether rules support promotion
```

A 0.99 model confidence from an untrusted source should not automatically beat a 0.80 extraction from an authoritative source.

## 8. Human approval design

Human review should be targeted, not universal.

Route to approval when:

- the source is low authority;
- identity resolution is ambiguous;
- the relation changes a high-impact policy;
- contradictions cannot be resolved automatically;
- the mutation crosses a defined risk threshold.

The approval should bind to the exact proposal hash/version so an approved proposal cannot be swapped after approval.

## 9. Idempotent graph writes

A retry after timeout creates a dangerous ambiguity:

```text
commit → timeout
   ?
Did the graph change?
```

Use stable proposal/action identity and reconcile before retrying.

```text
proposal_id + canonical payload hash + graph version
```

The same proposal should not create duplicate edges on repeated delivery.

## 10. Contradiction handling

Never solve contradiction by deleting one side.

```text
Claim A: System X owner = Team A
Claim B: System X owner = Team B
             |
             v
        contradiction
             |
      policy / review
```

Preserve evidence and record the resolution decision.

## 11. Rollback

Rollback is a new governed mutation, not history deletion.

A good rollback records:

- what changed;
- which proposal caused it;
- who/what authorized the reversal;
- restored version/hash;
- timestamp;
- residual impact.

## 12. Agent architecture

```text
                    TASK
                     |
                     v
              Source selector
                     |
                     v
              Agent extractor
               /          \
              v            v
          evidence      candidate KG
              |            |
              +------v-----+
                     |
                 validator
             /      |       \
          reject quarantine approve
                            |
                       commit gateway
                            |
                       graph version
                            |
                    health evaluator
                            |
                         rollback
```

The agent never gets direct unrestricted graph-write access.

## 13. Security threats

Threats include:

- prompt injection in source documents;
- fabricated citations;
- entity poisoning;
- relation poisoning;
- tenant escape;
- approval replay;
- proposal tampering;
- mass low-quality updates;
- rollback abuse;
- model/tool supply-chain compromise.

Controls: untrusted-data separation, provenance, schema validation, least privilege, tenant binding, proposal hashes, approval binding, rate limits, quarantine, immutable audit and independent verification.

## 14. Evaluation

Measure both extraction and downstream impact:

- entity precision/recall/F1;
- relation precision/recall/F1;
- unsupported-claim rate;
- provenance coverage;
- false merge rate;
- contradiction detection precision;
- promotion precision;
- quarantine rate;
- rollback success;
- graph health change;
- downstream retrieval/task success.

## 15. Failure-first challenge

Give the constructor deliberately hostile inputs: an injected instruction, unknown entity, cross-tenant source, contradictory policy, duplicate delivery and a high-confidence false relation. The learner must show that every unsafe proposal is stopped before graph commit.

## 16. Handoff to Module 34

Module 33 makes graph construction safe and measurable. Module 34 asks the next production question: **How should graph evidence and vector evidence be combined, ranked, filtered and evaluated for actual retrieval tasks?**
