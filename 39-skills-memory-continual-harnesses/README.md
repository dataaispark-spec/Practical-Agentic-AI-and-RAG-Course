# Module 39 — Skills, Memory & Continual Harnesses

## Why this matters
A long-running agent becomes useful when it can preserve validated knowledge and reusable procedures without turning stale or poisoned state into authority.

## Learning outcomes

By completing this module you can:

1. Distinguish working memory, episodic memory, semantic memory and procedural skills.
2. Design provenance, confidence, sensitivity, tenant scope, version and expiry for persistent state.
3. Convert experience into candidate skills through explicit evidence and evaluation.
4. Gate promotion from candidate to trusted behavior.
5. Detect contradictions, stale state and tenant-crossing memory.
6. Implement skill versioning, rollback and deprecation.
7. Measure reuse success, regression and stale-memory rates.
8. Explain why continual learning must remain reversible and policy-bounded.

## Core lifecycle

```text
Experience → Candidate Skill/Memory → Validate/Evaluate → Trusted State
→ Retrieve → Use → Observe → Improve / Rollback / Forget
```

## Hands-on labs

1. Build a versioned skill registry.
2. Add memory provenance and tenant scope.
3. Require evidence before promotion.
4. Add contradiction detection.
5. Add expiry and forgetting.
6. Add tenant-aware retrieval.
7. Simulate malicious learned procedures.
8. Compare static and continually learned skills on a fixed regression set.
9. Implement rollback after a harmful skill regression.
10. Measure promotion precision, reuse success, stale rate and security incidents.

## Failure-first

Low-confidence skill promotion, poisoned memory, stale procedure, benchmark overfit, silent overwrite, privilege drift and tenant leakage.

## Security

Persistent memory and skills are data stores, not authorization stores. Learned behavior must never grant itself permissions or bypass policy.

## Mastery gate

Demonstrate candidate→trusted promotion with evidence, reject unsafe learning, roll back a regression, enforce tenant scope and explain the governance boundary around continual learning.
