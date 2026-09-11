# Banking Lab — Durable Settlement Reconciliation

## Scenario
A settlement platform receives duplicate and delayed exception events. The agent may propose a correction, but only the deterministic control plane may commit it.

## Build
Partition by account/settlement ID. Use stable `effect_id`, durable checkpoint, lease/fence, monetary budget, reconciliation API and approval for high-value corrections.

## Failure injections
1. duplicate event;
2. timeout after correction was applied;
3. worker lease expires;
4. approval expires during wait;
5. ledger API outage.

## Required proof
Show the effect ledger and external ledger state before/after recovery. Demonstrate zero duplicate protected corrections and escalation of unresolved uncertainty.

## Metrics
Duplicate-effect rate, reconciliation latency, backlog age, cost/correction, approval-expiry rate, unresolved-risk count.
