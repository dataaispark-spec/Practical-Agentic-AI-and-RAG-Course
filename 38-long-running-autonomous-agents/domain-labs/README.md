# Module 38 Domain Labs — Production Failure Scenarios

These labs translate durable-agent mechanics into realistic business systems. Each lab must produce: **architecture → state contract → threat model → failure injection → recovery evidence → metrics → residual risk**.

## 1. Banking — Settlement exception worker

**Goal:** reconcile millions of synthetic settlement exceptions overnight.

**Build:** durable task identity, partitioned queue, effect ledger, ledger reconciliation, approval for high-value corrections, cumulative monetary/tool budgets.

**Inject:** duplicate event, timeout-after-write, ledger unavailable, approval expiry, worker takeover.

**Prove:** no duplicate protected correction; every uncertain correction is reconciled or escalated; monetary exposure is bounded.

**Measure:** correction duplicate rate, reconciliation latency, backlog age, cost/record, approval expiry rate.

## 2. Cybersecurity — Persistent SOC investigation

**Goal:** investigate a high-severity alert over several hours while waiting for analyst approval.

**Build:** evidence checkpoints, authenticated event wakeups, tenant/asset authorization, policy-version revalidation and containment effect IDs.

**Inject:** stale policy, poisoned checkpoint, duplicate alert, analyst approval expiry, provider outage.

**Prove:** stale authority cannot trigger containment; evidence provenance remains reconstructable.

## 3. SRE — Overnight migration/remediation

**Goal:** migrate a synthetic service fleet with prechecks, backup, change, verification and rollback.

**Build:** pre/postconditions, checkpoints, leases, cancellation contract and SLO deadline.

**Inject:** crash after change, stale worker, partial fleet failure, dependency outage.

**Prove:** resume does not repeat completed changes and failed verification triggers bounded recovery.

## 4. Enterprise IT — Change-management worker

**Goal:** process requests through approval, implementation and verification.

**Build:** durable waiting for CAB approval, action-hash binding, role revalidation, audit trail and DLQ.

**Inject:** approval replay, requester role change, duplicate ticket event, implementation timeout.

**Prove:** approval is tied to the exact authorized action and current policy.

## 5. Research — Long-horizon evidence collector

**Goal:** collect evidence from multiple sources over a long period and produce a verified conclusion.

**Build:** source provenance, evidence checkpoints, wait states, context compaction and verification gates.

**Inject:** source outage, contradictory evidence, stale checkpoint, malicious content and context overflow.

**Prove:** compaction does not erase authoritative evidence and contradictory claims are surfaced rather than silently merged.

## Cross-domain grading rubric

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| durability | happy path only | restart | recovery matrix | quantified recovery proof |
| side effects | naive retry | idempotency | reconciliation | business invariant proof |
| authority | implicit | stored | revalidated | versioned + expiry-aware |
| economics | ignored | per-run | cumulative | bounded under chaos |
| security | checklist | threats | controls | adversarial evidence |
| operations | logs | metrics | traces/SLOs | incident reconstruction |
