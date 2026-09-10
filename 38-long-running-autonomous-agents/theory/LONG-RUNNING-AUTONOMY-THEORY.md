# Module 38 — Long-Running Autonomy: Theory & Architecture

## Core idea
A durable agent is a distributed system with a reasoning component. The difficult problem is not keeping an LLM process alive; it is preserving task semantics across crashes, retries, waiting periods, workers, policy changes and uncertain external effects.

## Durable state model
`GOAL → TASK → RUN → ATTEMPT → CHECKPOINT → EFFECT → VERIFICATION`.
A checkpoint is semantic state, not merely a loop counter. It must identify the task version, state version, completed effects, pending work, authority/policy version, budgets and recovery position.

## Exactly-once reality
Most external systems provide at-least-once delivery. Therefore teach **effectively-once business semantics** using stable idempotency keys, reconciliation and durable effect records rather than claiming universal exactly-once execution.

## Lease/fencing invariant
Only the current lease holder may commit authoritative state. A stale worker must be rejected even if it resumes successfully after a network pause. Fencing/version tokens prevent zombie workers from performing late writes.

## Recovery matrix
| Failure point | Recovery |
|---|---|
| before effect | retry safely |
| during effect | reconcile external state |
| after effect/before checkpoint | detect idempotency record and continue |
| after checkpoint/before verification | re-verify |
| expired approval | stop and request fresh approval |
| stale policy | revalidate before effect |

## Long-horizon controls
Deadlines, cumulative token/tool/time/money budgets, wake-up limits, backpressure, retry caps, DLQs and human escalation must remain authoritative across restarts.

## Production invariants
1. Restart cannot duplicate a protected effect.
2. Resumption cannot inherit expired authority.
3. A waiting task consumes no unbounded active-worker capacity.
4. Every terminal outcome is reconstructable from trace + durable state.
5. Cancellation has defined effect semantics.

## Advanced exercises
Design lease fencing for 1M concurrent jobs; compare event sourcing with checkpoint snapshots; calculate retry amplification during a dependency outage; design disaster recovery with RPO/RTO; prove safe recovery for a timeout-after-write case.
