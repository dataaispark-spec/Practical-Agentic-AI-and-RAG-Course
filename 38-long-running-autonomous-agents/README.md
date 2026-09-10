# Module 38 — Long-Running Autonomous Agents

**Canonical implementation:** `38-long-running-autonomous-agents/`

## Mission
Move from request/response agents to durable workers that can operate for hours or days while remaining bounded, observable, recoverable and governable.

## Why this module matters
Long-running autonomy is a distributed-systems problem. A process restart, duplicate delivery, expired approval or timeout after an external write can change the meaning of the task. The learner must engineer **business-safe recovery**, not merely persistence.

## Learning outcomes
Design GOAL/TASK/RUN/ATTEMPT/CHECKPOINT identities; durable state machines; leases and fencing; heartbeats; event-driven waiting; checkpoint/replay; idempotent effects; reconciliation; approval expiry; cumulative budgets; backpressure/DLQ; cancellation; stale-worker detection; disaster recovery and incident reconstruction.

## Core architecture
```text
EVENT/SCHEDULE → DURABLE TASK → QUEUE → LEASE/FENCE → WORKER
                                      ↓          ↓
                                  CHECKPOINT   EFFECT
                                      ↓          ↓
                              WAIT/APPROVAL   VERIFY
                                      ↓          ↓
                             RESUME/RECOVER → COMPLETE/ESCALATE
```

**Invariant:** restart must never silently duplicate a protected external effect or resurrect expired authority.

## Component deep dive
| Component | Responsibility | Failure prevented |
|---|---|---|
| Durable task | stable objective/scope | lost work |
| Attempt | execution identity | ambiguous retries |
| Lease/fence | exclusive authority | zombie writes |
| Checkpoint | semantic recovery state | incorrect resume |
| Effect ledger | idempotency/reconciliation | duplicate side effects |
| Wait state | durable suspension | busy-looping |
| Budget ledger | cumulative limits | runaway cost |
| DLQ | terminal retry isolation | retry storms |
| Audit trail | reconstruction | invisible failures |

Read [`theory/LONG-RUNNING-AUTONOMY-THEORY.md`](theory/LONG-RUNNING-AUTONOMY-THEORY.md) before implementation.

## Practical labs
1. Durable lifecycle/state machine.
2. Lease + fencing race.
3. Crash before/during/after effect.
4. Timeout-after-write reconciliation.
5. Approval persistence and expiry.
6. Event/timer/webhook waiting.
7. Context compaction with authoritative-state preservation.
8. Goal-drift detection.
9. Multidimensional cumulative budgets.
10. Zombie worker detection.
11. Backpressure and DLQ.
12. Provider outage and backlog recovery.
13. 24-hour economics simulation.
14. Chaos/recovery benchmark.
15. Production architecture review.

## Domain tracks
- Banking: settlement/reconciliation worker.
- Cybersecurity: persistent SOC investigation.
- SRE: overnight remediation/migration.
- Enterprise IT: ticket and change-management worker.
- Research: multi-stage evidence collection with approval waits.

## Failure-first contract
Inject duplicate delivery, split brain, stale policy, checkpoint corruption, provider outage, tool timeout, approval expiry, cancellation race and uncertain external effects. Record **detection → containment → recovery → regression → residual risk**.

## Measures
Resume success, duplicate-effect rate, recovery success, recovery time, stale-worker rate, checkpoint overhead, escalation rate, backlog depth, cost/run and SLA compliance.

## Exercises
Design an overnight reconciliation platform for millions of records; compare snapshot checkpoints vs event sourcing; calculate retry amplification; design RPO/RTO; prove effectively-once business semantics.

## Security
Persisted state is security-sensitive. Revalidate tenant, permissions, policy version and approvals on resume. Never trust a stored model message as authority.

## Deliverables
Theory note, executable notebook, deterministic worker implementation, tests, recovery matrix, chaos evidence, cost model and production ADR.

## Mastery gate
Demonstrate safe stop/wait/resume/restart, no duplicate protected effects, stale-worker fencing, authority revalidation, bounded economics and reconstructable history.
