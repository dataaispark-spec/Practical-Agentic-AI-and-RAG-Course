# Module 4 — LLM Application Foundations: Build a Multi-Model Router

## Mission
Build the control layer that decides **which model should handle a request** while keeping application logic independent from provider SDKs. The router introduces capability matching, health-aware fallback, cost/latency policy, structured outputs, and measurable routing decisions.

## Learning outcomes

You will be able to:

1. Define model capabilities as explicit metadata.
2. Route requests by task requirements instead of model popularity.
3. Separate provider adapters from application logic.
4. Implement health-aware fallback without hiding failures.
5. Add cost and latency constraints to routing.
6. Preserve deterministic policy around probabilistic model behavior.
7. Test routing decisions without real model calls.
8. Explain model routing trade-offs in production system design.

## Architecture

```text
Application
   |
   v
Model Router
   |
   +--> capability filter
   +--> policy filter
   +--> health filter
   +--> cost/latency scoring
   |
   +----------+----------+
   |          |          |
   v          v          v
Provider A  Provider B  Local/Fake
   |          |          |
   +----------+----------+
              |
              v
        Typed response
```

## Why routing exists

A single model is rarely optimal for every workload. A production system may need:

- a low-cost model for classification
- a stronger model for complex reasoning
- a fast model for interactive requests
- a privacy-constrained model for sensitive data
- a fallback provider during an outage

The router is a **policy and infrastructure component**, not an LLM prompt.

## Model profile

Represent capabilities explicitly:

```python
ModelProfile(
    name="fast-model",
    provider="provider-a",
    max_context_tokens=32_000,
    supports_tools=True,
    supports_json=True,
    cost_per_1k_input=0.001,
    cost_per_1k_output=0.004,
    expected_latency_ms=700,
)
```

Do not encode critical routing assumptions only in prose.

## Routing decision

A request should carry requirements such as:

```text
task_type: extraction | chat | reasoning | coding
min_context_tokens
requires_tools
requires_json
max_latency_ms
max_cost_usd
privacy_class
```

Then:

```text
candidate models
      |
      v
capability filtering
      |
      v
privacy/policy filtering
      |
      v
health filtering
      |
      v
cost + latency scoring
      |
      v
selected model
```

If no model satisfies hard requirements, **fail clearly or escalate**. Do not silently violate a policy.

## Fallback semantics

Different failures deserve different behavior:

| Failure | Typical response |
|---|---|
| invalid request | fail immediately |
| unsupported capability | choose another compatible model |
| authentication failure | alert; do not blindly retry |
| transient 5xx | bounded fallback/retry |
| timeout | bounded fallback if deadline remains |
| policy violation | fail closed |

Fallback should preserve the original request's constraints.

## Cost-aware selection

A simplistic score can be:

```text
score = quality_weight × quality
      - latency_weight × normalized_latency
      - cost_weight × normalized_cost
```

But hard constraints should be applied **before** scoring. A model exceeding a privacy or maximum-cost constraint must not win because it has better quality.

## Lab — Multi-Model Router

Implement:

```text
app/
  models.py
  router.py
  providers.py

tests/
  test_router.py
```

Required features:

1. typed `ModelProfile`
2. typed `ModelRequest`
3. capability filtering
4. hard cost/latency constraints
5. health-aware selection
6. deterministic tie-breaking
7. fallback on transient provider failure
8. routing telemetry
9. fake providers for tests

## Reference implementation pattern

```python
candidates = registry.compatible(request)
if not candidates:
    raise NoCompatibleModel("no model satisfies hard requirements")

healthy = [m for m in candidates if health.is_healthy(m.name)]
ranked = sorted(healthy, key=lambda m: (m.expected_latency_ms, m.name))
return ranked[0]
```

The production version should incorporate measured quality, recent failure rate, cost, and remaining request deadline.

## Failure lab

### Failure 1 — Cheapest model always wins

**Symptom:** cost falls but task-success rate collapses.

**Lesson:** optimize cost per successful task, not price per token.

### Failure 2 — Fallback violates privacy

**Symptom:** sensitive data is sent to a provider that is not permitted for that privacy class.

**Fix:** privacy filtering must be a hard routing constraint.

### Failure 3 — Retry/fallback exceeds deadline

**Symptom:** three provider attempts make p95 latency worse than a single failure.

**Fix:** propagate a remaining deadline and stop when the budget is exhausted.

### Failure 4 — Routing feedback loop

**Symptom:** a temporarily slow provider is never selected again even after recovery.

**Fix:** health state needs decay, recovery probes, and explicit policy.

## Production metrics

Track:

- selected model/provider
- fallback count
- model selection latency
- provider latency
- task success by model
- cost per request
- cost per successful task
- error rate by provider
- policy rejection count
- routing decision reason

## Industry challenge

Design routing for an enterprise assistant with:

- public data: any approved model
- internal data: approved enterprise models only
- regulated data: private deployment only
- interactive requests: p95 under 2 seconds
- background requests: cost prioritized

Explain the hard constraints, scoring layer, fallback policy, and audit fields.

## Interview bank

1. Why do model routing systems exist?
2. What belongs in a model profile?
3. Which routing requirements should be hard constraints?
4. How do you avoid provider lock-in?
5. How do you design fallback?
6. Why can fallback increase outage severity?
7. How do you route by privacy class?
8. How do you optimize cost without destroying quality?
9. Why measure cost per successful task?
10. How would you detect a provider degradation?
11. How would you prevent a routing feedback loop?
12. How do you preserve an end-to-end deadline across fallback attempts?
13. What should be logged for a routing decision?
14. How do you test a router deterministically?
15. How would you run an A/B experiment on routing?
16. How do you handle a new model entering production?
17. How would you roll back a bad routing policy?
18. What is the difference between model capability and model quality?
19. How do you avoid hidden provider-specific assumptions?
20. Design a router for 100k requests/minute.

## Mastery gate

Build a router that can explain every selection and rejection, enforce hard constraints, fail over within a deadline, and prove through tests that forbidden models are never selected.
