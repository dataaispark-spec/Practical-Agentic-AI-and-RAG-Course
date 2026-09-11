# Module 38 — Long-Running Autonomous Agents

**Canonical path:** `38-long-running-autonomous-agents/`

## 1. Mission

Turn a short-lived agent into a **durable autonomous worker** that can operate for hours or days without losing task meaning when the process crashes, a dependency times out, an approval expires, a worker becomes stale, or an external side effect has an uncertain outcome.

This module is deliberately taught as a **distributed-systems + agent-harness problem**. An LLM may propose what to do; durable control-plane mechanisms decide whether, when and under what authority it may happen.

## 2. What learners must be able to explain

By the end, learners can:

1. distinguish goal, task, run, attempt, checkpoint and effect identity;
2. model a durable state machine with explicit terminal and waiting states;
3. explain why at-least-once delivery is normal and why "exactly once" execution is usually the wrong promise;
4. implement effectively-once business semantics with idempotency keys, effect ledgers and reconciliation;
5. prevent zombie workers with leases, heartbeats and fencing tokens;
6. make waiting durable instead of consuming an active worker indefinitely;
7. revalidate policy, tenant, scope and human approval after every resume boundary;
8. carry cumulative token/tool/time/money budgets across restarts;
9. design retries, backpressure, DLQs, cancellation and escalation as control-plane behavior;
10. reconstruct an incident from durable state, effect records and an append-only audit trail;
11. reason about RPO/RTO, multi-region recovery and disaster scenarios;
12. benchmark recovery correctness, latency, cost and duplicate-effect risk.

## 3. Mental model

```text
                  CONTROL PLANE
Goal → Task → Run → Policy → Budget → Lease/Fence → Decision
                       │                         │
                       ▼                         ▼
                 Durable State              Action Gateway
                       │                         │
                       ▼                         ▼
              Checkpoint / Wait ←────── Effect Ledger ──────→ External System
                       │                         │
                       └────────── Verify / Reconcile ──────┘
                                      │
                         Complete / Retry / Recover /
                         Replan / Escalate / Cancel
```

**Core invariant:** a restart may repeat computation, but it must not silently repeat a protected business effect or resurrect expired authority.

## 4. Durable state contract

Use the identity chain:

`GOAL → TASK → RUN → ATTEMPT → CHECKPOINT → EFFECT → VERIFICATION`

A checkpoint is **semantic recovery state**, not just `step=37`. It should preserve at least:

- task and tenant identity;
- task/schema/state version;
- current state and recovery position;
- completed and uncertain effects;
- idempotency keys;
- policy/permission version;
- approval binding and expiry information;
- cumulative budgets and deadlines;
- pending external events;
- correlation/trace identifiers.

## 5. Reference implementation

`app/worker.py` is a deterministic, dependency-free teaching implementation. It demonstrates:

- `DurableStore` as an authoritative state store;
- lease acquisition, renewal and fencing;
- monotonic checkpoints;
- an effect ledger with `pending/applied/unknown/reconciled` states;
- timeout-after-write reconciliation;
- pause/resume/cancel;
- approval binding to an action hash and policy version;
- cumulative step/tool/cost budgets;
- retry-amplification calculation.

It is intentionally **not** presented as a production database or queue. The learner must map the same invariants to PostgreSQL/Redis/Kafka/workflow engines/cloud queues in the architecture exercises.

## 6. Failure semantics — the heart of the module

| Failure boundary | Unsafe naive behavior | Correct teaching pattern |
|---|---|---|
| before external effect | retry | retry with stable effect ID |
| during effect | assume failure | mark outcome uncertain and reconcile |
| after effect, before checkpoint | execute again | consult effect ledger/idempotency record |
| after checkpoint, before verification | trust state | re-verify externally |
| worker pause after lease expiry | continue writing | fencing rejects stale writer |
| approval expires while waiting | reuse approval | stop and obtain fresh approval |
| policy changes during downtime | resume blindly | re-authorize against current policy |
| provider outage | uncontrolled retries | bounded retry + backpressure + escalation |
| cancellation race | partial/unknown semantics | define per-effect cancellation contract |
| corrupted checkpoint | execute arbitrary state | schema/version/provenance validation |

## 7. Labs — 15 increasing-difficulty builds

1. **Durable lifecycle:** implement `created → running → waiting → completed/failed/cancelled/dead-letter`.
2. **Checkpoint recovery:** compare every-step, every-N and event-log recovery.
3. **Crash matrix:** inject failures before, during and after effects.
4. **Effect ledger:** prove a retry cannot duplicate a protected effect.
5. **Timeout-after-write:** reconcile an external correction whose response was lost.
6. **Lease + fencing:** create a split-brain worker race and reject the stale writer.
7. **Durable waiting:** sleep for approval, timer, webhook and customer response without holding a worker.
8. **Authority revalidation:** invalidate an approval or policy version while the job is asleep.
9. **Cumulative economics:** carry token/tool/compute/money limits across multiple attempts.
10. **Backpressure:** process a 10,000-event burst without retry amplification or unbounded concurrency.
11. **Provider outage:** compare pause, fallback, queue, degradation and escalation policies.
12. **Long-horizon migration:** make every migration stage resumable with pre/postconditions and rollback.
13. **Stale/poisoned state:** attack persisted checkpoints and require provenance + schema validation.
14. **Incident reconstruction:** rebuild a failure timeline from state, effects and trace events.
15. **Chaos day:** combine lease loss, duplicate delivery, outage, approval expiry, cancellation and uncertain effects.

## 8. Domain labs

See [`domain-labs/README.md`](domain-labs/README.md) for detailed tracks in:

- banking settlement/reconciliation;
- cybersecurity/SOC investigations;
- SRE migration and remediation;
- enterprise IT change management;
- research/evidence collection.

Each track requires a **failure matrix + recovery proof + SLO/cost analysis**, not merely a working happy path.

## 9. Benchmarking

See [`benchmarks/README.md`](benchmarks/README.md). Measure:

- duplicate protected effects;
- recovery correctness and resume distance;
- recovery time;
- stale-worker rejection;
- uncertain-effect reconciliation rate;
- checkpoint overhead;
- queue backlog and p95 latency;
- cost per completed task;
- SLA/SLO compliance;
- retry amplification.

Never report a benchmark without workload size, seed, failure injection point, environment and recovery evidence.

## 10. Security model

Long-running state is an **authority-bearing security boundary**. Treat stored model output as untrusted data. On resume, re-check tenant isolation, object scope, permissions, policy version, approval freshness and action hash. Protect effect ledgers and checkpoints from tampering. Audit both accepted and rejected actions.

Threats include stale authority, checkpoint poisoning, cross-tenant replay, lease hijacking, duplicate financial effects, approval replay, budget bypass and malicious wake-up/event injection.

## 11. Production architecture exercise

Design a multi-region service processing millions of durable tasks. Defend:

- queue semantics and ordering requirements;
- task/effect identity and idempotency boundaries;
- lease/fencing implementation;
- storage consistency model;
- event-driven waiting;
- retry/backoff/DLQ policy;
- cumulative budgets;
- cancellation semantics;
- tenant isolation and authorization revalidation;
- audit/event retention;
- RPO/RTO and region failover;
- observability and incident reconstruction;
- cost and capacity model.

## 12. Deliverables

- theory notes;
- executable Colab notebook;
- deterministic reference implementation;
- comprehensive tests;
- failure/recovery matrix;
- domain-lab evidence pack;
- benchmark results with reproducibility metadata;
- security/threat model;
- production architecture decision record;
- mastery-gate defense.

## 13. Mastery gate

A learner passes only when they can **demonstrate and explain** safe stop/wait/resume/restart, timeout-after-write reconciliation, stale-worker fencing, approval/policy revalidation, cumulative budget enforcement, cancellation semantics and reconstructable recovery history.

### L7 challenge

Design and defend a multi-region durable-agent platform for millions of tasks under at-least-once delivery. The design must remain safe when a worker crashes after an external write, a lease expires during a network partition, a human approval becomes stale, a provider is unavailable for an hour, and one region is lost. Quantify the residual risk rather than claiming impossible guarantees.

## Module handoff

M38 supplies the **durability substrate** for later modules: M39 adds skills/memory/continual state, M40 adds environments and verifiers, M41 adds controlled self-improvement, M42 adds computer-use action loops, and M43 composes the full frontier system.
