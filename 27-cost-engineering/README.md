# Module 27 — Cost Engineering: Cost-Aware AI Router

## Mission

Make economics a first-class control signal. Route each task to the least expensive architecture that can satisfy quality, latency, safety and capability requirements.

**Objective:** minimize cost subject to constraints, not simply choose the cheapest model.

```text
Task
 ↓
Requirements extraction
 ↓
Candidate models / retrieval / tools
 ↓
Policy + capability filter
 ↓
Cost × quality × latency × risk scoring
 ↓
Budget check
 ↓
Route / escalate / fallback / abstain
 ↓
Observe actual cost
 ↓
Evaluate outcome
```

## Learning outcomes

- Model token, tool and infrastructure costs.
- Calculate cost per successful task.
- Build deterministic budget enforcement.
- Route between small/large models.
- Use caching and batching safely.
- Detect retry amplification and runaway loops.
- Design quality-aware escalation.
- Compare cost-quality frontiers.
- Attribute spend to tenant, agent, model and tool.
- Prevent cost optimization from bypassing safety.

## Cost model

At minimum track:

```text
input tokens
output tokens
model price
embedding cost
reranker cost
tool/API cost
compute cost
storage cost
retry cost
cache hit/miss
```

A useful derived metric is:

`cost_per_success = total_cost / successful_tasks`

## Routing objective

For candidate route `r`:

`utility(r) = expected_quality - λ(cost) - μ(latency) - ν(risk)`

subject to hard constraints:

- capability;
- privacy;
- policy;
- budget;
- latency SLO;
- minimum quality.

Hard constraints must be applied **before** economic ranking.

## Routing patterns

### Fixed routing
Simple but often wasteful.

### Capability routing
Choose by context length, modality, tool support or reasoning capability.

### Cost-aware routing
Use the lowest-cost route satisfying constraints.

### Cascade
Start cheap, escalate only when confidence/verification is insufficient.

### Speculative parallelism
Run alternatives concurrently when latency value justifies extra cost.

### Cache-first
Reuse valid prior work before calling a model/tool.

## Detailed labs

### Lab 1 — Cost ledger
Implement token/model/tool pricing and cost calculation.

### Lab 2 — Per-task attribution
Calculate cost per run, agent, tenant and capability.

### Lab 3 — Budget enforcement
Hard-stop a run before it exceeds monetary/token/tool budgets.

### Lab 4 — Model router
Choose between small, medium and large models based on requirements.

### Lab 5 — Quality-aware cascade
Escalate when verification confidence is below threshold.

### Lab 6 — Cache economics
Calculate savings and stale-cache risk.

### Lab 7 — Retry amplification
Measure how transient failures multiply spend.

### Lab 8 — Loop economics
Inject a repeated agent loop and stop it with a budget.

### Lab 9 — Cost-quality frontier
Compare routes using cost per successful task.

### Lab 10 — Tenant budgets
Apply independent budgets and prevent cross-tenant consumption.

### Lab 11 — Tool economics
Include expensive external APIs in route selection.

### Lab 12 — Shadow routing
Evaluate a cheaper route without changing production behavior.

### Lab 13 — FinOps dashboard
Create daily spend, unit economics and anomaly views.

### Lab 14 — Abuse simulation
Simulate prompt inflation, tool-call storms and adversarial cost attacks.

### Lab 15 — Optimization review
Produce an optimization proposal with savings, quality impact, risk and rollback.

## Failure-first exercises

- cheapest model produces unacceptable quality;
- model price changes;
- cache serves stale sensitive information;
- retry storm multiplies spend;
- tool cost dominates model cost;
- tenant exceeds budget;
- cost router selects a model forbidden by privacy policy;
- parallel execution doubles spend for negligible latency gain;
- budget accounting is inconsistent after restart;
- cost metric omits failed requests.

## Production guardrails

Never allow cost optimization to override:

**security → authorization → privacy → correctness → hard safety constraints.**

A cheaper unauthorized action is still unauthorized.

Use:

- hard budgets;
- soft budgets;
- per-task caps;
- tenant quotas;
- concurrency limits;
- circuit breakers;
- cache controls;
- anomaly alerts;
- emergency kill switches.

## Industry scenarios

**Banking:** route low-risk FAQ tasks to economical models while transaction workflows use stricter capability and verification constraints.

**Healthcare:** minimize cost only after privacy and evidence requirements are satisfied.

**Cybersecurity:** allow expensive reasoning when incident severity justifies it; never downgrade mandatory security controls merely to save money.

**Enterprise IT:** use cache/read tools first, then inexpensive models, then escalate for ambiguous remediation.

## Interview bank

1. Why isn't cheapest-model routing sufficient?
2. What is cost per successful task?
3. How do you account for retries?
4. How can caching create hidden risk?
5. When is parallelism economically justified?
6. How do you enforce tenant budgets?
7. What should happen after a budget is exhausted?
8. How do you combine quality and cost?
9. How do you detect cost anomalies?
10. How do you prevent an attacker from creating token/tool spend?
11. How do you route under privacy constraints?
12. How would you optimize a system spending $1M/month?

## Coding challenges

- pricing ledger;
- cost calculator;
- budget object;
- cost-aware router;
- quality cascade;
- cache ROI calculator;
- retry cost analyzer;
- anomaly detector;
- tenant quota manager;
- cost-per-success evaluator.

## Mastery gate

Given multiple models and tools with different prices, quality, latency and constraints, design a router that meets task requirements while minimizing cost and proving that safety/policy constraints were never traded away.

## Gold challenge

Build **AegisAI Cost Control Plane** connected to Modules 25–26. It must forecast and attribute spend, enforce budgets, route intelligently, detect anomalies and evaluate whether savings actually preserve task success and safety.
