# Module 38 — Long-Running Autonomy: Theory, Mechanics & Production Design

## 1. The architectural shift

A request/response agent has a short lifetime: receive input, reason, call tools, return output. A long-running agent has a **durability boundary** between every meaningful stage. The process can disappear at any instant and another process may continue the same business task later.

Therefore:

> **Long-running autonomy is not "a bigger agent loop". It is a durable workflow whose decisions happen to include probabilistic model reasoning.**

The production control plane must remain deterministic enough to enforce identity, authority, budgets, concurrency and recovery even when model output is wrong or unavailable.

## 2. Identity model

Do not collapse all identifiers into one job ID.

```text
GOAL       = durable business objective
TASK       = bounded unit of work within the goal
RUN        = one logical execution lifecycle
ATTEMPT    = one worker ownership/execution attempt
CHECKPOINT = recoverable semantic state
EFFECT     = one externally meaningful side effect
VERIFY     = evidence that the effect/outcome is correct
```

A useful effect identity is:

`effect_id = hash(tenant, task_id, action_type, business_object, action_version)`

The exact formula depends on the business domain. The invariant is that retries of the **same intended business effect** resolve to the same identity, while genuinely different effects do not collide.

## 3. State machine

A durable worker should expose explicit states rather than infer state from logs.

```text
CREATED → RUNNING → CHECKPOINTED ───────→ COMPLETED
             │             │
             │             ├────────────→ WAITING → RUNNING
             │             ├────────────→ RETRY
             │             └────────────→ ESCALATED
             ├──────────────────────────→ CANCELLED
             └──────────────────────────→ DEAD_LETTER
```

Transitions need guards. Examples:

- `RUNNING → WAITING` only after durable wait intent is committed;
- `WAITING → RUNNING` only after the wake condition is validated;
- `RUNNING → COMPLETED` only after required verification succeeds;
- `RUNNING → RETRY` only when retry policy allows it;
- `WAITING → RUNNING` must revalidate authority rather than inherit stale authority.

## 4. Checkpoint semantics

A checkpoint is a **recovery contract**. It should answer: "If every worker process disappears now, what can the next worker safely do?"

Minimum conceptual fields:

```text
schema_version
state_version
task_id / tenant_id
current_state
next_recovery_position
completed_effect_ids
uncertain_effect_ids
pending_event_ids
policy_version
approval_binding
budget_ledger
deadline
correlation_id
```

Compare three strategies:

| Strategy | Recovery loss | Write cost | Replay complexity | Best use |
|---|---:|---:|---:|---|
| every step | low | high | low | high-risk short tasks |
| every N steps | bounded | medium | medium | batch processing |
| event log | low | high | high | complex workflows/audit |

The right choice is a business-risk decision, not a fashionable storage decision.

## 5. Exactly-once: teach the real guarantee

At-least-once delivery means the same message may arrive more than once. Network failure can also create **uncertain outcomes**: the client times out after the server accepted the request.

There are three different properties:

1. **Exactly-once execution** — the action physically happens once. Often impossible to guarantee across independent systems.
2. **Exactly-once delivery** — the message is delivered once. Often not guaranteed by queues.
3. **Effectively-once business semantics** — repeated attempts resolve to one business effect. This is the useful engineering target.

Typical pattern:

```text
claim intent → stable effect ID → external operation
       │                         │
       └──── durable ledger ←────┘
                    │
             verify / reconcile
```

The effect ledger must itself have suitable consistency and durability. An in-memory `set()` is not a production idempotency system; it is only a teaching simplification.

## 6. The timeout-after-write problem

This is the canonical long-running-agent failure:

```text
Worker → POST /correct-account
Server → applies correction
Network → response lost
Worker → sees timeout
Worker → retries POST
```

Without an idempotency key or reconciliation API, the worker cannot know whether the first operation happened.

Correct recovery options, in descending preference:

1. idempotent API with the same key;
2. query/reconciliation endpoint using a durable business reference;
3. transactional outbox/inbox pattern where applicable;
4. human/manual reconciliation for high-risk irreversible effects.

**Never** equate "timeout" with "operation did not happen."

## 7. Leases, heartbeats and fencing

A lease says who currently owns execution. A heartbeat says the worker still believes it is alive. Neither alone prevents stale writes.

Consider:

```text
A owns fence=41
A network partition
lease expires
B acquires fence=42
A resumes
```

A must be unable to commit authoritative state. The authoritative store checks the fencing token on the write. This is stronger than merely checking a timestamp in the worker process.

A production design must also define:

- lease duration;
- renewal cadence;
- clock assumptions;
- what happens during partitions;
- takeover delay;
- maximum stale-worker window;
- fencing enforcement at the final write boundary.

## 8. Durable waiting

Waiting for a human, timer, webhook or external job should become a durable state, not a sleeping thread.

```text
RUNNING
   ↓ commit wait intent
WAITING(reason, correlation_id, deadline)
   ↓ event/timer
WAKE → validate event → revalidate authority → RUNNING
```

This saves worker capacity and creates an auditable boundary. Wake events must be deduplicated and correlated to the correct task/tenant.

## 9. Authority is time-dependent

An approval granted yesterday is not automatically valid today. Persisted state can outlive:

- the user's role;
- the approval TTL;
- the policy version;
- the target object's ownership;
- the risk classification;
- the allowed action parameters.

Bind high-impact approval to the **exact action representation** (for example an action hash) and reauthorize it at execution time.

Never let a stored model message become an authority token.

## 10. Cumulative budgets

A long-running task can exceed limits even if every individual attempt looks safe. Track cumulative budgets across attempts:

`B = (tokens, tool_calls, compute_seconds, money, wall_clock, wakeups, retries)`

A budget ledger should be monotonic and durable. Define behavior when a budget is exhausted:

- stop safely;
- wait for an operator;
- reduce scope;
- switch to a cheaper policy/model;
- escalate.

A retry must not reset the budget.

## 11. Retry amplification

If an outage causes retries and each attempt fans out, load can grow faster than the original workload. A simple educational model is:

`attempts = N × (1 + f + f² + ... + f^r)`

where `N` is initial work, `f` is fan-out and `r` is the number of retry rounds.

Use exponential backoff, jitter, retry budgets, circuit breakers, concurrency caps and DLQs where appropriate. Do not automatically retry non-idempotent effects.

## 12. Cancellation semantics

"Cancel" is not a universal rollback.

For each effect classify:

- **not started** → can cancel;
- **in flight** → may become uncertain;
- **committed and reversible** → compensate if safe;
- **committed and irreversible** → record outcome and escalate.

The cancellation contract must be explicit in the workflow and tested at race boundaries.

## 13. Long-horizon context

A multi-day agent cannot keep appending every observation to a single prompt. Separate:

- authoritative task state;
- compact working memory;
- raw evidence/archive;
- decisions and rationale;
- external source of truth.

Context compaction must not delete the facts needed to recover safely. The durable state is authoritative; model context is a derived view.

## 14. Backpressure and dead-letter design

When arrival rate exceeds service capacity:

`queue depth ↑ → latency ↑ → retries ↑ → load ↑`

Break the loop with admission control, per-tenant concurrency limits, queue partitioning, backoff, circuit breakers and DLQ routing. A DLQ is not a trash can: it requires ownership, reason codes, retention, replay rules and security controls.

## 15. Disaster recovery

Define RPO/RTO per state class.

- Losing a derived prompt summary may be acceptable.
- Losing an effect ledger for a financial correction may be catastrophic.
- Losing an approval audit trail may create compliance exposure.

Replication strategy should follow business invariants. Multi-region architecture does not automatically solve split-brain or duplicate effects.

## 16. Observability

Minimum trace dimensions:

`task_id, run_id, attempt_id, effect_id, tenant_id, worker_id, fence, state_version, policy_version, outcome`

Measure both operational and semantic outcomes:

- recovery success rate;
- duplicate-effect rate;
- uncertain-effect rate;
- stale-worker rejection rate;
- time-to-recovery;
- checkpoint overhead;
- queue age/p95 latency;
- cost per successful task;
- approval expiry rate;
- DLQ rate;
- SLA compliance.

A beautiful trace that cannot prove whether a payment was duplicated is not sufficient observability.

## 17. Security threats

| Threat | Control |
|---|---|
| checkpoint poisoning | integrity, schema validation, provenance |
| cross-tenant replay | tenant-bound identifiers and authorization |
| approval replay | expiry + action hash + policy version |
| stale worker write | fencing at authoritative store |
| budget bypass | durable cumulative ledger |
| malicious wake event | authenticated correlation + authorization |
| effect duplication | idempotency/reconciliation |
| model prompt injection | treat retrieved/persisted content as untrusted |

## 18. What the learner should implement vs only design

**Implement:** state machine, checkpoint, effect ledger, fencing simulation, approval binding, budget ledger, retry model, reconciliation and tests.

**Design:** multi-region storage, queue partitioning, transactional outbox, production database schema, operational SLOs and disaster-recovery runbooks.

This separation keeps the notebook deterministic while still reaching production architecture depth.

## 19. Mastery test

A learner should be able to take one failure timeline and answer, with evidence:

1. What was the exact business task?
2. Which worker had authority?
3. Which effects were definitely applied?
4. Which outcomes were uncertain?
5. Which checkpoint was authoritative?
6. Was the approval still valid?
7. Which budgets remained?
8. Why was the recovery action safe?
9. What duplicate-effect risk remains?
10. Which invariant would fail first at 10× scale?

That is the standard for durable-agent engineering.
