# Module 38 — Long-Running Autonomous Agents

## Mission
Move from request/response agents to durable workers that can operate for long periods while remaining bounded, observable, recoverable and governable.

## Learning outcomes

By completing this module you can:

1. Distinguish goals, tasks, runs, attempts and checkpoints.
2. Design durable state that survives process restart.
3. Implement worker leases, heartbeats and stale-worker detection.
4. Enforce multidimensional budgets over long-running work.
5. Implement safe checkpoint, pause, cancel and resume semantics.
6. Make external side effects idempotent or compensate for them.
7. Persist human approvals and revalidate policy before resuming.
8. Handle event-driven waiting and scheduled wake-ups.
9. Recover from crashes, provider failures and changed external state.
10. Reconstruct execution history for audit and debugging.
11. Measure recovery rate, duplicate effects, SLA adherence and cost/run.
12. Defend long-running autonomy decisions in system design.

## Core abstraction

```text
Goal → durable state → loop → environment/tools
     → verification → checkpoint/recovery → completion
```

## Hands-on lab — Durable Autonomous Worker

Build a worker with a durable queue/state store, leases, heartbeats, checkpoints, waiting states, approval persistence, policy revalidation, idempotency keys, replayable events and bounded retry/recovery.

### Failure-first cases

Duplicate execution, split brain, lost progress, goal drift, infinite autonomy, stale policy, stale knowledge, zombie workers, provider outage and uncertain external side effects.

### Metrics

Completion rate, recovery success, recovery time, duplicate-effect rate, checkpoint overhead, cost/run, escalation rate and SLA adherence.

## Frontier case studies

Use Hermes Agent, Prime Agent and always-on agent patterns as architectural case studies. For each capability identify the persistence/control primitive that enables it and the new failure mode introduced.

## Security

Persistence does not create authority. Revalidate identity, tenant, policy, approval and external state after pause/resume or restart.

## Mastery gate

Prove safe stop/restart/wait/resume behavior, no duplicate side effects in the tested workflow, stale-state detection, policy revalidation and reconstructable execution history.
