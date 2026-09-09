# Module 36 — Loop Engineering

**Canonical implementation:** `36-loop-engineering/`. Former `31-loop-engineering/` is legacy only.

## Mission
Build the deterministic execution kernel beneath an agent: `OBSERVE → DECIDE → POLICY → ACT → VERIFY → RECOVER → CONTINUE/STOP`.

## Learning outcomes
You will be able to design explicit state transitions, bounded execution, policy gates, typed actions, independent verification, retry taxonomy, checkpoints, recovery, replay, budgets, kill switches and auditable trajectories.

## Architecture
```text
Goal → Observe → Model proposal → Policy → Action Gateway
 ↑                                      ↓
 └──── Recover ← Verify ← Environment/Tool
              ↓
 Checkpoint + Audit + Budget + Deadline + Kill switch
```

## Labs
1. SOC investigation loop.
2. SRE rollback loop with approval.
3. Coding-agent repair loop.
4. Banking reconciliation with independent verification.
5. Typed model proposals and invalid-action rejection.
6. Retry/timeout/idempotency taxonomy.
7. Independent postconditions.
8. Infinite-loop and no-progress detection.
9. Crash recovery around side effects.
10. Prompt-injection/security boundary.
11. Cost per successful iteration.
12. Replayable trajectory telemetry.
13. Fixed vs reactive vs guarded adaptive benchmark.
14. Production architecture review.
15. Failure-injection day.

## Failure contract
Inject provider outage, stale observation, tool timeout, duplicate delivery, malformed action, budget exhaustion, authorization denial, false verification, worker crash and corrupted checkpoint. For every failure record detection, containment, retry/stop decision and residual risk.

## Measures
Success rate, false containment, tool calls, p95 latency, tokens, cost/task, recovery rate, escalation rate and verifier agreement.

## Exercises / system design
Design an autonomous SOC investigator for 10,000 alerts/day. Defend termination, concurrency, identity, approval gates, evidence quality, cost controls and auditability.

## Security
User input, retrieved documents, memory and tool outputs are untrusted data. None may redefine policy, tenant, budget or approval requirements.

## Mastery gate
Demonstrate bounded execution, explicit state transitions, independent verification, correct retries, durable recovery, policy isolation, auditable trajectories and measurable quality/cost/safety trade-offs.
