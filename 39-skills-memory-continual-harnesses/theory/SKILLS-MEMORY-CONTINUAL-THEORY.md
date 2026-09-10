# Module 39 — Skills, Memory & Continual Harnesses: Theory

## Taxonomy
**Memory** records information from experience; **skill** encodes a reusable procedure; **policy** defines authority. These must never collapse into one store.

### Memory layers
- episodic: what happened;
- semantic: validated facts;
- procedural: reusable methods;
- working: current task context;
- governance: provenance, scope, expiry and policy metadata.

## Lifecycle
`OBSERVED → CANDIDATE → EVALUATED → TRUSTED → DEPRECATED/EXPIRED → REVOKED`.
Promotion requires evidence and regression tests. Reuse must preserve tenant scope and provenance.

## Skill contract
A skill should declare trigger, preconditions, inputs, steps, expected outcomes, failure handling, permissions, version, provenance and evaluation evidence. A model-generated procedure is not automatically trusted executable policy.

## Continual-learning boundary
Separate **learning plane** from **execution plane**. The learning plane proposes changes; the execution plane remains governed and can only consume promoted artifacts.

```text
TRAJECTORIES → MINING → CANDIDATE → EVALUATION → PROMOTION
                                  ↘ REJECT/QUARANTINE
TRUSTED SKILLS → HARNESS → OUTCOME → REGRESSION FEEDBACK
```

## Failure modes
Memory poisoning, stale memory, contradictory memories, semantic drift, skill regression, privilege drift, cross-tenant retrieval and feedback-loop amplification.

## Invariants
1. Memory cannot change identity or authorization.
2. Candidate skill cannot execute privileged actions.
3. Promotion is versioned and reversible.
4. Retrieval respects tenant/ACL scope before ranking.
5. Deprecated knowledge remains auditable where policy requires retention.

## Exercises
Build a SOC skill promotion pipeline; resolve two contradictory runbooks; design expiry for procedures; measure reuse value against retrieval/token cost; create a rollback after a promoted skill causes regression.
