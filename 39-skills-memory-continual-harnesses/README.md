# Module 39 — Skills, Memory & Continual Harnesses

**Canonical implementation:** `39-skills-memory-continual-harnesses/`. Former `34-skills-memory-continual-harnesses/` is legacy only.

## Mission
Make persistent knowledge and reusable procedures governed, versioned and reversible rather than silent sources of authority.

## Learning outcomes
Distinguish skills from memory; build candidate/trusted/rejected/deprecated states; require provenance and evaluation; support promotion, rollback, reuse, contradiction handling, forgetting and tenant/security controls.

## Architecture
```text
Experience → Candidate Skill → Evaluation/Verifier → Promotion Gate
     ↓                              ↓                    ↓
Memory ← Evidence/Outcome ← Regression Suite → Trusted Registry
```

## Labs
1. Versioned skill registry.
2. Candidate generation from successful trajectories.
3. Provenance and confidence.
4. Promotion gates.
5. Contradictory skills/memory.
6. Stale-procedure detection.
7. Tenant-aware memory retrieval.
8. Poisoned skill injection.
9. Rollback after regression.
10. Forgetting/expiry policy.
11. Static vs continually learned skill benchmark.
12. Reuse quality and cost measurement.

## Exercises
Add skill versioning, provenance requirements, contradiction detection, tenant isolation, regression gates and rollback. Demonstrate that an untrusted memory item cannot silently become executable policy.

## Measures
Promotion precision, regression rate, reuse success, stale-skill rate, rollback frequency, memory hit rate, latency, token cost and security violations.

## Security
Persistence expands attack surface: memory poisoning, skill injection, privilege drift and cross-tenant retrieval must be blocked by deterministic policy and verification.

## Mastery gate
Implement and defend a continual harness in which learned state is attributable, evaluated, reversible, tenant-scoped and policy-bounded.
