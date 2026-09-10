# Module 35 — Compounding Knowledge / LLM Wiki Theory

## 1. Why this module exists

A RAG system can answer from documents without creating durable organizational knowledge. A compounding knowledge system is different: each accepted piece of evidence can improve an existing knowledge base while preserving provenance, uncertainty, history, contradictions, and rollback.

This module is **Karpathy-inspired**, not an official Karpathy methodology. The engineering goal is to teach a durable knowledge-maintenance architecture that sits between raw sources, retrieval, agents, and later graph/hybrid systems.

## 2. Core architecture

```text
                    SOURCE PLANE
 raw docs / APIs / tickets / policies / observations
                         |
                         v
                +-------------------+
                | Evidence Registry |
                | source + hash +    |
                | tenant + timestamp |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Claim Extraction   |
                | entity + relation  |
                | claim + confidence |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Validation / Gate  |
                | provenance         |
                | schema             |
                | contradiction      |
                | authority/policy   |
                +----+----------+----+
                     |          |
                reject|          |accept
                     v          v
              quarantine   Knowledge Store
                               |
              +----------------+----------------+
              |                |                |
              v                v                v
          Claims           Entity Pages      Change Log
              |                |                |
              +----------------+----------------+
                               |
                               v
                      Context Compiler
                               |
                    bounded, cited context
                               |
                               v
                       RAG / Agent / Graph
                               |
                               v
                    Feedback + evaluation
                               |
                               +----> next update
```

## 3. The key architectural distinction

**Documents are evidence. Claims are normalized knowledge. Pages are compiled views.**

Never treat a generated wiki page as the original evidence. A page must be reproducible from its accepted claims and their evidence references.

## 4. Core components and responsibilities

| Component | Responsibility | Critical invariant |
|---|---|---|
| Evidence Registry | immutable source identity and metadata | evidence is addressable and traceable |
| Claim Model | normalized atomic assertion | every claim has provenance |
| Entity Resolver | stable identity for subjects/objects | aliases do not silently create duplicates |
| Validator | schema, evidence, authority and quality checks | invalid claims never become active knowledge |
| Contradiction Detector | identify incompatible claims | conflict is visible, not silently overwritten |
| Knowledge Store | active + historical claims | updates preserve history |
| Page Compiler | produce human/agent-readable pages | compiled text is not authoritative by itself |
| Context Compiler | select bounded evidence-backed context | context has provenance and size limits |
| Change Log | record promotions, supersessions, rejections, rollback | every mutation is auditable |
| Health Evaluator | freshness, provenance, contradiction and coverage metrics | knowledge quality is measurable |
| Rollback Manager | reverse bad promotions | rollback is reversible and evidence-preserving |

## 5. Claim lifecycle

```text
DISCOVERED → NORMALIZED → VALIDATED → ACTIVE
                         |             |
                         v             v
                     QUARANTINED   SUPERSEDED
                         |             |
                         +----REJECTED+

ACTIVE → CONTRADICTED → REVIEW → ACTIVE or SUPERSEDED
ACTIVE → ROLLED_BACK → prior valid state
```

A claim should carry at least: `claim_id`, `topic/entity`, `text`, `source_id`, `source_hash`, `observed_at`, `valid_from`, optional `valid_to`, confidence, status, version, and update metadata.

## 6. Compounding is not append-only storage

A naive system does:

`new document → append text → retrieve more text`

A compounding system does:

`new evidence → compare → normalize → validate → merge/supersede/conflict → compile → evaluate`

The second approach prevents knowledge bloat and makes change explicit.

## 7. Provenance and authority

Provenance answers **where did this claim come from?** Authority answers **why should this source be trusted for this claim?** They are not the same.

A high-confidence claim with weak provenance is still unsafe. A highly authoritative source can also be stale or contradictory. Keep source identity, evidence span/hash, authority metadata and freshness separate.

## 8. Contradictions

Do not resolve contradictions by last-write-wins. Store both claims, expose the conflict, and apply an explicit resolution policy such as source authority, temporal validity, corroboration, or human review.

Example:

```text
Policy A: retention = 90 days
Policy B: retention = 30 days
          |
          v
      contradiction
          |
    authority + date
          |
     review decision
          |
  active claim + history
```

## 9. Freshness and temporal semantics

Knowledge has at least three useful times:

- `observed_at`: when the evidence was observed
- `valid_from`: when the claim became true
- `valid_to`: when it ceased to be true, if known

A newly ingested source can therefore supersede old knowledge without erasing the historical record.

## 10. Entity resolution and duplicate concepts

Aliases, naming changes and duplicate concepts are a major source of wiki drift. Resolve identity before merging claims. Keep an alias map and an explicit confidence/decision trail. Never silently merge two entities solely because their names look similar.

## 11. Page compilation

A page is a deterministic projection of accepted knowledge:

```text
entities + active claims + citations + conflicts + freshness
                         |
                         v
                   page compiler
                         |
                         v
                 bounded wiki page
```

The compiler should make it possible to regenerate the page after rollback or source correction.

## 12. Context compilation for agents

Agent context should contain only the minimum useful, validated knowledge. Prefer:

`claim → evidence reference → freshness → confidence`

over an uncited prose summary. Context budgets must be explicit so the wiki does not become a new form of context bloat.

## 13. Security model

Threats include poisoned sources, fabricated citations, cross-tenant leakage, unauthorized promotion, stale authoritative documents, malicious updates, prompt injection embedded in sources, and rollback abuse.

Security controls:

1. tenant/source isolation;
2. immutable evidence identity;
3. provenance required for promotion;
4. validation before activation;
5. policy/authority checks;
6. quarantine for suspicious updates;
7. append-only audit events;
8. least-privilege mutation paths;
9. bounded context compilation;
10. rollback with authorization and audit.

## 14. Measurement

Minimum production metrics:

- provenance coverage = claims with valid evidence / active claims;
- freshness SLA = active claims within freshness policy / active claims;
- contradiction rate = conflicted active topics / active topics;
- duplicate rate = unresolved duplicate entities / entities;
- promotion precision = correctly accepted claims / accepted claims;
- rejection precision/recall on a labeled safety set;
- rollback success rate;
- context compression ratio;
- answer/task success with raw RAG vs curated wiki;
- update latency and human-review load.

## 15. Required experiment

Hold the questions, source corpus and evaluator constant. Compare:

1. raw-document RAG;
2. curated wiki;
3. knowledge graph;
4. KG + vector hybrid.

Measure answer/task accuracy, provenance coverage, freshness, contradiction handling, context size, latency and failure recovery. A wiki is not automatically better; its value must be demonstrated.

## 16. Failure modes to break intentionally

- append-only stale claims;
- citation loss;
- duplicate entities;
- contradictory authoritative sources;
- poisoned claim injection;
- cross-tenant evidence;
- context bloat;
- generated text treated as evidence;
- rollback to an invalid snapshot;
- silent last-write-wins;
- stale active claims after supersession.

## 17. Relationship to the surrounding course

- M31 introduces knowledge engineering and graph-RAG foundations.
- M32 adds graph engineering, ontology evolution and temporal knowledge.
- M33 turns extraction into governed graph construction.
- M34 combines graph and vector retrieval.
- **M35 turns evidence into maintained, compounding organizational knowledge.**
- M36 then focuses on the execution loop that operates over such state.
- M37 adds the broader agent harness around loops, tools, state and verification.
- M38 extends operation across long-running autonomous lifecycles.
- M39 adds skills, memory and continual harnesses.

## 18. Mastery standard

A learner has mastered M35 when they can design and implement a system that:

1. ingests evidence without losing provenance;
2. extracts and validates atomic claims;
3. resolves entities and duplicates explicitly;
4. represents contradictions and temporal validity;
5. compiles bounded wiki pages and agent context;
6. measures freshness, provenance and quality;
7. survives poisoning and tenant-isolation attacks;
8. rolls back bad updates without destroying history;
9. compares curated knowledge against raw RAG and graph/hybrid baselines;
10. explains why compounding knowledge is a governed data lifecycle, not autonomous note generation.
