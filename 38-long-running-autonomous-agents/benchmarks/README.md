# Module 38 Benchmark Contract

## Objective
Evaluate whether a durable worker preserves **business correctness under interruption**, not merely whether it eventually returns a result.

## Reproducibility
Every run must record:

- workload seed;
- task count and task size;
- worker concurrency;
- checkpoint policy;
- retry/backoff policy;
- lease TTL and renewal interval;
- failure injection point;
- provider/tool behavior;
- environment/runtime version.

## Baselines

1. checkpoint after every successful effect;
2. checkpoint every N effects;
3. append-only event-log replay;
4. naive retry baseline (included only as a negative control).

## Required failure matrix

| Injection | Primary metric | Expected invariant |
|---|---|---|
| crash before effect | resume correctness | effect eventually applied once |
| crash after effect | duplicate-effect rate | no duplicate protected effect |
| timeout after write | reconciliation rate | uncertain effect resolved |
| lease loss | stale-write count | stale writer rejected |
| expired approval | unsafe-action count | old approval never reused |
| provider outage | backlog recovery | bounded retry amplification |
| budget exhaustion | over-budget spend | cumulative limit respected |
| poisoned checkpoint | unsafe resume | invalid state rejected |

## Metrics

- `duplicate_effect_rate = duplicate_protected_effects / protected_effects`
- `recovery_success_rate = safely_recovered_tasks / interrupted_tasks`
- `resume_distance` (effects replayed after interruption)
- recovery p50/p95/p99;
- stale-worker rejection count;
- uncertain-effect reconciliation rate;
- checkpoint writes per task;
- queue age and p95 completion latency;
- cost per completed task;
- retry amplification factor;
- SLA/SLO compliance.

## Correctness gate

A benchmark cannot be called a pass because the final count matches. The result must show the **effect ledger, recovery trace and external-state reconciliation** for injected failures.

## Suggested experiment

Run 1,000 tasks with deterministic seeds. Interrupt 10% at randomly selected lifecycle boundaries, including 20% timeout-after-write cases. Compare all baselines. Report correctness first, then latency and cost. Explain why the cheapest strategy is not necessarily the safest.
