# Module 39 — Skills, Memory & Continual Harnesses

**Canonical implementation:** `39-skills-memory-continual-harnesses/`

## Mission
Turn experience into governed reusable knowledge and procedures without allowing memory or learned skills to become silent authority.

## Why this module matters
A durable agent accumulates information. A production agent must know **what happened, what is believed, what procedure is trusted, what has expired, and what is allowed**. Memory, skill and policy are different artifacts.

## Learning outcomes
Design episodic/semantic/procedural memory; versioned skill registries; provenance and temporal validity; candidate/trusted/rejected/deprecated states; contradiction handling; tenant-aware retrieval; expiry/forgetting; promotion gates; regression suites; rollback and continual feedback loops.

## Core architecture
```text
TRAJECTORY → EXPERIENCE → CANDIDATE MEMORY/SKILL
                         ↓
              PROVENANCE + VALIDATION
                         ↓
                  REGRESSION SUITE
                         ↓
               PROMOTE / REJECT / EXPIRE
                         ↓
              TRUSTED REGISTRY → HARNESS
                         ↘ ROLLBACK
```

**Invariant:** learned state can inform execution but cannot redefine identity, authorization, policy or budget.

## Component deep dive
| Component | Responsibility | Failure prevented |
|---|---|---|
| Episodic memory | records events/outcomes | loss of experience |
| Semantic memory | validated facts | repeated rediscovery |
| Skill registry | reusable procedures | ad-hoc unsafe procedures |
| Provenance | source/trajectory attribution | fabricated authority |
| Promotion gate | trust transition | poisoned learning |
| Regression suite | behavioral protection | skill regressions |
| Expiry/revocation | lifecycle control | stale procedures |
| Tenant scope | isolation | cross-customer leakage |

Read [`theory/SKILLS-MEMORY-CONTINUAL-THEORY.md`](theory/SKILLS-MEMORY-CONTINUAL-THEORY.md).

## Labs
1. Memory taxonomy and ownership.
2. Versioned skill registry.
3. Candidate skill mined from trajectories.
4. Provenance/confidence/temporal validity.
5. Promotion gate with regression tests.
6. Contradictory memory resolution.
7. Stale-skill detection and expiry.
8. Tenant-aware retrieval.
9. Memory/skill poisoning.
10. Rollback after regression.
11. Static vs continual skill benchmark.
12. Reuse quality/cost measurement.
13. Forgetting policy design.
14. Production continual-harness review.

## Domain tracks
SOC playbooks; SRE runbooks; customer support procedures; enterprise sales knowledge; synthetic regulated-workflow procedures.

## Failure-first contract
Inject poisoned memory, stale procedures, contradictory facts, cross-tenant hits, privilege drift and unsafe promotion. Capture detection, containment, recovery, regression and residual risk.

## Measures
Promotion precision, regression rate, reuse success, stale rate, rollback success, memory hit rate, retrieval quality, latency, token cost and security violations.

## Exercises
Design a continual SOC playbook learner; define a promotion policy; prove a rejected skill cannot execute; measure whether memory actually improves task success enough to justify its maintenance cost.

## Mastery gate
Demonstrate attributable, evaluated, reversible, tenant-scoped memory and skills integrated into a governed harness.
