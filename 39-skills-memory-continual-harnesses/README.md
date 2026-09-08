# Module 39 — Skills, Memory & Continual Harnesses

## Why this matters
A long-running agent becomes useful only when it can preserve validated knowledge and reusable procedures without turning stale or poisoned state into authority.

## Theory and mental model

**Experience → candidate skill → validation/evaluation gate → trusted skill → persistent memory → later retrieval → measured reuse**

A skill is a reusable procedure. Memory stores evidence and context. A continual harness decides what may be learned, promoted, rolled back, or forgotten.

## Architecture / data flow

```text
Task
  ↓
Agent loop → memory retrieval → candidate procedure
  ↓                         ↑
Tool execution → outcome/evidence
  ↓
Candidate skill → verifier/evaluation gate
  ↓
Trusted skill registry → persistent store
  ↓
Future tasks + regression evaluation
```

## Industry scenario
An enterprise support agent repeatedly diagnoses the same production incident. It may propose a troubleshooting skill, but promotion requires evidence, security checks, regression tests, provenance, versioning and rollback.

## Build
Implement a skill registry with explicit states such as `candidate`, `trusted`, `rejected`, and `deprecated`. Attach provenance, confidence, evaluation evidence and version identifiers.

## Break / debug
Inject a low-confidence skill, contradictory memory, stale procedure, malicious instruction and tenant-crossing memory. Verify that untrusted knowledge cannot silently become executable policy.

## Measure
Track skill promotion precision, regression rate, reuse success, stale-skill rate, rollback frequency, memory retrieval hit rate, latency, token cost and security violations.

## Security
Persistence expands the attack surface: memory poisoning, skill injection, privilege drift, cross-tenant retrieval and unsafe learned procedures must be blocked by policy and verification gates.

## Exercises
1. Add skill versioning and rollback.
2. Require provenance for promotion.
3. Add contradiction detection between skills.
4. Add tenant-aware retrieval.
5. Compare static skills against continually learned skills using a fixed regression set.

## Interview / system design
- When should an agent learn a skill versus keep the behavior ephemeral?
- How do you prevent memory from becoming an untrusted policy store?
- Design rollback for a skill that caused a production regression.
- What evidence is sufficient to promote a candidate skill?

## Mastery gate
You can explain, implement, break, measure and defend a continual harness while keeping learned state reversible, attributable and policy-bounded.
