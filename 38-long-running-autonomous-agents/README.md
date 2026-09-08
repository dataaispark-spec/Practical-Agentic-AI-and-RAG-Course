# Module 38 — Long-Running Autonomous Agents

**Canonical implementation:** `38-long-running-autonomous-agents/`. Former `33-long-running-autonomous-agents/` is legacy only.

## Mission
Move from request/response agents to durable workers that can operate for hours or days while remaining bounded, observable, recoverable and governable.

## Learning outcomes
Implement durable GOAL/TASK/RUN/ATTEMPT/CHECKPOINT identities; leases, heartbeats, deadlines, multidimensional budgets, checkpoints, resumability, idempotent side effects, pause/resume/cancel, approvals, scheduling, stale-state detection, policy revalidation and audit reconstruction.

## Architecture
```text
Goal → Task → Durable Run → Lease/Heartbeat → Agent Loop
                         ↓
             Checkpoint → Tool/Environment → Verify
                         ↓
               Wait / Recover / Resume / Stop
```

## Labs
1. Durable lifecycle and state machine.
2. Worker leases and heartbeats.
3. Duplicate-delivery/idempotency handling.
4. Crash recovery at side-effect boundaries.
5. Human approval persistence and expiry.
6. Event-driven waiting and scheduling.
7. Context compaction without losing authoritative state.
8. Goal-drift detection.
9. Multidimensional budget exhaustion.
10. Stale worker/zombie detection.
11. Reconciliation after uncertain external effects.
12. Replay and incident reconstruction.
13. Chaos/failure injection.
14. Recovery benchmark.
15. Production architecture review.

## Exercises
Break duplicate execution, split brain, lost progress, stale policy, stale knowledge, infinite autonomy, zombie workers and uncertain external side effects. Document detection, containment and recovery.

## Measures
Completion rate, duplicate side effects, recovery success, recovery time, checkpoint overhead, escalation rate, cost/run and stale-state rate.

## Security
Persistence changes the threat model: approvals, permissions, policy versions, expiry and tenant boundaries must survive restarts. A resumed run must revalidate authority rather than trusting stale state.

## Mastery gate
Demonstrate safe stop/restart/wait/resume, bounded autonomy, no duplicate side effects, policy revalidation and reconstructable execution history.
