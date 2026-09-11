# Module 38 — Long-Running Autonomous Agents

## Module boundary

M38 teaches how to turn an agent into a **durable, bounded, recoverable worker** that can run across crashes, retries, waiting periods and changing authorization. The module is about long-running execution semantics—not knowledge compounding, skills, continual learning, recursive self-improvement, computer use, or reinforcement learning.

## Why this is hard

A short-lived agent can keep most state in process memory. A long-running agent cannot. Between two steps, the process may die, a worker may be replaced, a lease may expire, an external write may have happened without a response, an approval may become invalid, or a dependency may remain unavailable for hours. Recovery must preserve **business semantics**, not merely program counters.

## Learning outcomes

By the end, learners can:

1. Model `GOAL → TASK → RUN → ATTEMPT → CHECKPOINT → EFFECT → VERIFICATION`.
2. Design durable state machines and explicit wait/resume/cancel semantics.
3. Explain at-least-once delivery versus exactly-once execution and effectively-once business effects.
4. Implement stable effect identities, idempotency and timeout-after-write reconciliation.
5. Implement leases, heartbeats and fencing to reject zombie workers.
6. Revalidate tenant, identity, policy version and approval before resuming sensitive work.
7. Enforce cumulative time, tool, token and monetary budgets across restarts.
8. Design backpressure, bounded retries and dead-letter handling.
9. Reconstruct incidents from durable state, effect records and traces.
10. Defend RPO/RTO, SLO, cost and failure semantics for production-scale workers.

## Core architecture

```text
Trigger
  ↓
Durable Task ──→ Queue ──→ Lease/Fence ──→ Worker
     │                         │              │
     ├── policy/approval ──────┘              │
     ├── cumulative budget ───────────────────┤
     └── checkpoint / wait                    ↓
                                      Action Gateway
                                             ↓
                                       Effect Ledger
                                             ↓
                                       External API
                                             ↓
                                     Verify / Reconcile
                                             ↓
                              Checkpoint / Retry / Recover
                                             ↓
                                   Complete / Escalate / DLQ
```

**Primary invariant:** a restart must not silently duplicate a protected business effect or resurrect expired authority.

## Durable state model

A checkpoint is semantic recovery state. It should identify the task version, current state, completed effects, uncertain effects, pending work, authority/policy version, cumulative budgets and recovery position. A counter such as `step=37` is not enough to establish safe recovery.

| Identity | Purpose |
|---|---|
| Goal ID | stable business objective |
| Task ID | scoped executable contract |
| Run ID | logical execution lifecycle |
| Attempt ID | worker execution attempt |
| Checkpoint ID | recoverable state snapshot/version |
| Effect ID | stable external business-effect identity |
| Fence token | current worker authority |
| Approval ID | authorization bound to exact action/version |

## Exactly-once reality

Teach the guarantee boundary explicitly:

- **Delivery:** queues commonly provide at-least-once delivery.
- **Execution:** a worker can crash or be retried.
- **Effect:** an external system may commit before the client receives a response.
- **Business semantics:** stable effect IDs, idempotent APIs and reconciliation can provide effectively-once behavior for a defined business operation.

Do not claim universal exactly-once execution across arbitrary distributed systems.

## Recovery matrix

| Failure point | Correct reasoning | Recovery pattern |
|---|---|---|
| Before effect | no protected effect committed | retry if still authorized |
| During effect | outcome may be unknown | reconcile before retry |
| After effect, before checkpoint | effect may already exist | effect ledger/idempotency lookup |
| After checkpoint, before verification | state may be ahead of verification | re-verify |
| Lease expired | worker may be stale | fence old worker; new owner resumes |
| Approval expired | authority no longer valid | stop and request fresh approval |
| Policy changed | prior decision may be invalid | revalidate policy before effect |
| Dependency outage | retries can amplify load | backoff, queue, pause or escalate |
| Cancellation race | effect may be irreversible | classify state; do not assume rollback |

## Labs

### Foundation
1. Durable task lifecycle and state machine.
2. Semantic checkpoints and recovery positions.
3. Stable effect identity and idempotency.
4. Crash-before/during/after-effect matrix.

### Distributed-systems mechanics
5. Timeout-after-write reconciliation.
6. Lease, heartbeat and fencing race.
7. Durable waiting for approval, timer and webhook.
8. Stale-worker and stale-checkpoint rejection.

### Production controls
9. Cumulative budgets and retry amplification.
10. Backpressure, fairness, bounded retries and DLQ.
11. Cancellation and irreversible-effect semantics.
12. Provider outage and backlog recovery.

### Long-horizon operations
13. Resumable migration with pre/postconditions.
14. Incident reconstruction from durable evidence.
15. Multi-failure chaos day and production architecture review.

## Domain labs

- **Banking:** settlement-exception reconciliation with timeout-after-write and approval expiry.
- **Cybersecurity:** persistent SOC investigation with policy revalidation before containment.
- **SRE:** overnight migration/remediation with rollback classification and SLA budget.
- **Enterprise IT:** durable change-management workflow with CAB approval and fencing.
- **Research:** long-running evidence collection with provenance and durable waits.

Each domain lab must produce a failure matrix, recovery proof, metrics, cost/SLO analysis and residual-risk statement.

## Engineering implementation

The reference implementation is deterministic and dependency-light. It exposes the mechanisms directly rather than hiding them behind an orchestration framework: state transitions, effect ledger, lease/fence checks, reconciliation and budget accounting.

## Failure-first requirements

Inject duplicate delivery, crash-after-effect, timeout-after-write, lease loss, stale worker, expired approval, policy change, corrupted checkpoint, provider outage, cancellation race, budget exhaustion and retry storm.

For every failure record:

`detection → containment → recovery decision → evidence → regression test → residual risk`.

## Measurement

Track recovery success rate, duplicate protected-effect rate, uncertain-effect reconciliation rate, stale-worker rejection rate, resume latency, recovery time, checkpoint write amplification, replay distance, queue age, retry amplification, cost per completed task, escalation/DLQ rate and SLO compliance.

## Security boundary

Persisted state is untrusted input. On resume, validate schema/version, tenant scope, identity, authorization, policy version and approval freshness. Never treat an old model-generated message as durable authority. High-impact actions must be bound to an exact action representation and current policy.

## L7 system design

Design a multi-region durable-agent platform processing millions of tasks under at-least-once delivery. Defend storage consistency, fencing, idempotency, ordering, event-driven waiting, retries/DLQ, tenant isolation, approval revalidation, observability, RPO/RTO, failover and economics. State which guarantees are impossible or conditional.

## Required deliverables

Theory notes; executable Colab notebook; deterministic reference implementation; comprehensive tests; recovery matrix; five domain labs; reproducible benchmark; chaos evidence; production ADR; mastery evidence pack.

## Mastery gate

Pass only when the learner demonstrates safe stop/wait/resume/restart, no duplicate protected effects under tested failure modes, timeout-after-write reconciliation, stale-worker fencing, authority revalidation, cumulative budget enforcement, explicit cancellation semantics, bounded retries/backpressure and reconstructable history.

## Explicit exclusions

M38 does **not** teach continual learning, skills systems, recursive self-improvement, agentic RL, computer-use automation, multi-agent coordination or knowledge-graph construction. Those belong to other modules and should not be duplicated here.
