# Module 38 Mastery Gate — Long-Running Autonomous Agents

## Pass standard

This is an **evidence-based gate**, not a quiz. The learner must submit the notebook, tests, failure matrix, benchmark report, threat model and production ADR.

### A. Implementation gate — 30 points

- [ ] durable lifecycle/state machine — 5
- [ ] semantic checkpoint/restart — 5
- [ ] effect ledger + stable idempotency — 5
- [ ] timeout-after-write reconciliation — 5
- [ ] lease/heartbeat/fencing — 5
- [ ] cumulative budgets + cancellation — 5

### B. Failure gate — 25 points

Demonstrate all of:

- [ ] crash before effect;
- [ ] crash after effect but before checkpoint;
- [ ] uncertain external outcome;
- [ ] stale worker after lease takeover;
- [ ] expired approval/policy change;
- [ ] provider outage/retry storm;
- [ ] corrupted or poisoned checkpoint;
- [ ] cancellation race.

For each: **detection → containment → recovery → verification → regression test → residual risk**.

### C. Benchmark gate — 15 points

Report workload, seed, environment, failure injection, recovery correctness, duplicate-effect rate, recovery time, checkpoint overhead, backlog and cost. A final row count without semantic evidence is insufficient.

### D. Security gate — 10 points

Threat-model checkpoint poisoning, approval replay, cross-tenant replay, stale-worker writes, budget bypass and malicious wake events. Show controls at the authoritative boundary.

### E. Architecture defense — 20 points

Defend a multi-region service processing millions of tasks under at-least-once delivery. Cover queue semantics, storage consistency, fencing, idempotency, waiting, retries/DLQ, tenancy, audit, SLOs, RPO/RTO and failover.

## Critical-failure rule

Automatic fail if the submitted system:

- knowingly repeats a protected side effect after an uncertain outcome;
- accepts a stale fencing token;
- reuses expired approval without reauthorization;
- can reset cumulative budgets by restarting;
- treats model text as authority;
- claims universal exactly-once guarantees without qualification.

## L7 oral defense

Given this incident:

> Worker A writes a financial correction, times out, loses its lease, Worker B takes over, the approval expires, and the primary region fails before verification.

Explain exactly what state survives, what B may do, how the external ledger is reconciled, how authority is revalidated, what happens during regional recovery, and what evidence proves no duplicate correction occurred.
