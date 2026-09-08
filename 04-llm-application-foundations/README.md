# Module 4 — LLM Application Foundations



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

## Expanded long-form course chapter

This course is a practical engineering progression from deterministic software and LLM applications to retrieval, tools, stateful agents, distributed coordination, knowledge graphs, durable autonomy, verification, computer use, and controlled self-improvement. The governing idea is that an AI system becomes production-grade not by adding more model calls, but by adding explicit boundaries around probabilistic decisions. Throughout the 43 modules, the learner repeatedly asks: What is the goal? What state is authoritative? What evidence is available? What actions are permitted? What budget applies? What must be verified? What happens when a dependency fails? What must be observable and auditable? What evidence would justify changing the design?

The course uses the AegisAI mental model: Model + Harness + Environment + Tools + State + Policy + Budget + Verification. Retrieval is treated as a knowledge mechanism; an agent loop is treated as a decision-and-action mechanism; a harness is treated as the control plane around the model; and a verifier is treated as an independent check on outcomes. This distinction prevents a common engineering failure in which a prompt is asked to perform authorization, correctness checking, persistence, and business policy simultaneously.

Every module follows the same learning rhythm: Predict → Run → Observe → Explain → Break → Debug → Measure → Improve → Defend. The examples therefore emphasize observable mechanisms, explicit contracts, failure injection, metrics, and regression tests. The notebooks and applications are intended to work with deterministic fakes and synthetic data wherever possible, so that the learner can understand the mechanism before depending on a commercial provider.

## Module-specific learning contract

This expanded chapter deepens the repository canonical learning objectives for **Module 4: LLM Application Foundations**. The objective vocabulary is preserved: LLM application foundations, model routing, capabilities, fallback, cost, and latency. Each concept is connected to architecture, implementation, failure analysis, evaluation, security, operations and system-design reasoning.

## First-principles concepts

### 1. Llm Application Foundations

The first principle for LLM Application Foundations is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, LLM application foundations should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Model Routing

A practical way to learn LLM Application Foundations is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for model routing; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Capabilities

In an enterprise setting, LLM Application Foundations rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. capabilities becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Fallback

The failure-first perspective is especially important for LLM Application Foundations. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For fallback, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Cost

Measurement should accompany every meaningful change to LLM Application Foundations. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For cost, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Latency

A useful architecture diagram for LLM Application Foundations separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For latency, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Llm Application Foundations

Versioning is part of the technical design of LLM Application Foundations, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If LLM application foundations changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Model Routing

The final production question for LLM Application Foundations is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For model routing, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Architecture and control boundaries

### 1. Llm Application Foundations

The first principle for LLM Application Foundations is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, LLM application foundations should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Model Routing

A practical way to learn LLM Application Foundations is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for model routing; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Capabilities

In an enterprise setting, LLM Application Foundations rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. capabilities becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Fallback

The failure-first perspective is especially important for LLM Application Foundations. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For fallback, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Cost

Measurement should accompany every meaningful change to LLM Application Foundations. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For cost, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Latency

A useful architecture diagram for LLM Application Foundations separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For latency, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Llm Application Foundations

Versioning is part of the technical design of LLM Application Foundations, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If LLM application foundations changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Model Routing

The final production question for LLM Application Foundations is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For model routing, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Mechanisms and implementation reasoning

### 1. Llm Application Foundations

The first principle for LLM Application Foundations is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, LLM application foundations should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Model Routing

A practical way to learn LLM Application Foundations is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for model routing; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Capabilities

In an enterprise setting, LLM Application Foundations rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. capabilities becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Fallback

The failure-first perspective is especially important for LLM Application Foundations. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For fallback, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Cost

Measurement should accompany every meaningful change to LLM Application Foundations. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For cost, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Latency

A useful architecture diagram for LLM Application Foundations separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For latency, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Llm Application Foundations

Versioning is part of the technical design of LLM Application Foundations, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If LLM application foundations changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Model Routing

The final production question for LLM Application Foundations is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For model routing, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Industry scenarios and worked examples

### 1. Llm Application Foundations

The first principle for LLM Application Foundations is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, LLM application foundations should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Model Routing

A practical way to learn LLM Application Foundations is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for model routing; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Capabilities

In an enterprise setting, LLM Application Foundations rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. capabilities becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Fallback

The failure-first perspective is especially important for LLM Application Foundations. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For fallback, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Cost

Measurement should accompany every meaningful change to LLM Application Foundations. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For cost, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Latency

A useful architecture diagram for LLM Application Foundations separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For latency, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Llm Application Foundations

Versioning is part of the technical design of LLM Application Foundations, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If LLM application foundations changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Model Routing

The final production question for LLM Application Foundations is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For model routing, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Failure-first engineering

### 1. Llm Application Foundations

The first principle for LLM Application Foundations is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, LLM application foundations should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Model Routing

A practical way to learn LLM Application Foundations is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for model routing; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Capabilities

In an enterprise setting, LLM Application Foundations rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. capabilities becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Fallback

The failure-first perspective is especially important for LLM Application Foundations. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For fallback, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Cost

Measurement should accompany every meaningful change to LLM Application Foundations. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For cost, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Latency

A useful architecture diagram for LLM Application Foundations separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For latency, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Llm Application Foundations

Versioning is part of the technical design of LLM Application Foundations, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If LLM application foundations changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Model Routing

The final production question for LLM Application Foundations is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For model routing, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Experiments and measurement

### 1. Llm Application Foundations

The first principle for LLM Application Foundations is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, LLM application foundations should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Model Routing

A practical way to learn LLM Application Foundations is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for model routing; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Capabilities

In an enterprise setting, LLM Application Foundations rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. capabilities becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Fallback

The failure-first perspective is especially important for LLM Application Foundations. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For fallback, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Cost

Measurement should accompany every meaningful change to LLM Application Foundations. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For cost, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Latency

A useful architecture diagram for LLM Application Foundations separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For latency, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Llm Application Foundations

Versioning is part of the technical design of LLM Application Foundations, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If LLM application foundations changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Model Routing

The final production question for LLM Application Foundations is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For model routing, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Security, governance and responsible operation

### 1. Llm Application Foundations

The first principle for LLM Application Foundations is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, LLM application foundations should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Model Routing

A practical way to learn LLM Application Foundations is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for model routing; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Capabilities

In an enterprise setting, LLM Application Foundations rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. capabilities becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Fallback

The failure-first perspective is especially important for LLM Application Foundations. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For fallback, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Cost

Measurement should accompany every meaningful change to LLM Application Foundations. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For cost, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Latency

A useful architecture diagram for LLM Application Foundations separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For latency, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Llm Application Foundations

Versioning is part of the technical design of LLM Application Foundations, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If LLM application foundations changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Model Routing

The final production question for LLM Application Foundations is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For model routing, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Production design and operational readiness

### 1. Llm Application Foundations

The first principle for LLM Application Foundations is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, LLM application foundations should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Model Routing

A practical way to learn LLM Application Foundations is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for model routing; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Capabilities

In an enterprise setting, LLM Application Foundations rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. capabilities becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Fallback

The failure-first perspective is especially important for LLM Application Foundations. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For fallback, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Cost

Measurement should accompany every meaningful change to LLM Application Foundations. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For cost, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Latency

A useful architecture diagram for LLM Application Foundations separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For latency, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Llm Application Foundations

Versioning is part of the technical design of LLM Application Foundations, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If LLM application foundations changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Model Routing

The final production question for LLM Application Foundations is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For model routing, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Debugging and incident analysis

### 1. Llm Application Foundations

The first principle for LLM Application Foundations is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, LLM application foundations should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Model Routing

A practical way to learn LLM Application Foundations is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for model routing; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Capabilities

In an enterprise setting, LLM Application Foundations rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. capabilities becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Fallback

The failure-first perspective is especially important for LLM Application Foundations. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For fallback, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Cost

Measurement should accompany every meaningful change to LLM Application Foundations. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For cost, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Latency

A useful architecture diagram for LLM Application Foundations separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For latency, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Llm Application Foundations

Versioning is part of the technical design of LLM Application Foundations, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If LLM application foundations changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Model Routing

The final production question for LLM Application Foundations is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For model routing, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Exercises and independent practice

### 1. Llm Application Foundations

The first principle for LLM Application Foundations is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, LLM application foundations should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Model Routing

A practical way to learn LLM Application Foundations is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for model routing; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Capabilities

In an enterprise setting, LLM Application Foundations rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. capabilities becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Fallback

The failure-first perspective is especially important for LLM Application Foundations. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For fallback, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Cost

Measurement should accompany every meaningful change to LLM Application Foundations. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For cost, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Latency

A useful architecture diagram for LLM Application Foundations separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For latency, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Llm Application Foundations

Versioning is part of the technical design of LLM Application Foundations, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If LLM application foundations changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Model Routing

The final production question for LLM Application Foundations is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For model routing, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## System-design review

### 1. Llm Application Foundations

The first principle for LLM Application Foundations is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, LLM application foundations should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Model Routing

A practical way to learn LLM Application Foundations is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for model routing; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Capabilities

In an enterprise setting, LLM Application Foundations rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. capabilities becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Fallback

The failure-first perspective is especially important for LLM Application Foundations. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For fallback, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Cost

Measurement should accompany every meaningful change to LLM Application Foundations. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For cost, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Latency

A useful architecture diagram for LLM Application Foundations separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For latency, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Llm Application Foundations

Versioning is part of the technical design of LLM Application Foundations, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If LLM application foundations changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Model Routing

The final production question for LLM Application Foundations is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For model routing, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Assessment and mastery

### Question 1

Explain how you would design, implement, test, observe and defend **LLM application foundations** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 2

Explain how you would design, implement, test, observe and defend **model routing** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 3

Explain how you would design, implement, test, observe and defend **capabilities** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 4

Explain how you would design, implement, test, observe and defend **fallback** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 5

Explain how you would design, implement, test, observe and defend **cost** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 6

Explain how you would design, implement, test, observe and defend **latency** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 7

Explain how you would design, implement, test, observe and defend **LLM application foundations** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 8

Explain how you would design, implement, test, observe and defend **model routing** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 9

Explain how you would design, implement, test, observe and defend **capabilities** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 10

Explain how you would design, implement, test, observe and defend **fallback** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 11

Explain how you would design, implement, test, observe and defend **cost** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 12

Explain how you would design, implement, test, observe and defend **latency** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 13

Explain how you would design, implement, test, observe and defend **LLM application foundations** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 14

Explain how you would design, implement, test, observe and defend **model routing** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 15

Explain how you would design, implement, test, observe and defend **capabilities** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 16

Explain how you would design, implement, test, observe and defend **fallback** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 17

Explain how you would design, implement, test, observe and defend **cost** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 18

Explain how you would design, implement, test, observe and defend **latency** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 19

Explain how you would design, implement, test, observe and defend **LLM application foundations** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 20

Explain how you would design, implement, test, observe and defend **model routing** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 21

Explain how you would design, implement, test, observe and defend **capabilities** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 22

Explain how you would design, implement, test, observe and defend **fallback** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 23

Explain how you would design, implement, test, observe and defend **cost** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 24

Explain how you would design, implement, test, observe and defend **latency** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 25

Explain how you would design, implement, test, observe and defend **LLM application foundations** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 26

Explain how you would design, implement, test, observe and defend **model routing** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 27

Explain how you would design, implement, test, observe and defend **capabilities** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 28

Explain how you would design, implement, test, observe and defend **fallback** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 29

Explain how you would design, implement, test, observe and defend **cost** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 30

Explain how you would design, implement, test, observe and defend **latency** in a real LLM Application Foundations system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

## Mastery gate

Completion means being able to explain the mechanism from first principles, implement the smallest working version, deliberately break it, identify the first failing boundary from evidence, repair it, measure the repaired system against a baseline, and defend the resulting trade-offs. The learner should also explain when not to use the mechanism. Production expertise includes recognizing when a simpler deterministic solution is safer, cheaper and easier to operate.

## Deep case study 1: Llm Application Foundations

Consider an enterprise workload in which LLM application foundations is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why LLM application foundations cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 2: Model Routing

Consider an enterprise workload in which model routing is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why model routing cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 3: Capabilities

Consider an enterprise workload in which capabilities is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why capabilities cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 4: Fallback

Consider an enterprise workload in which fallback is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why fallback cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 5: Cost

Consider an enterprise workload in which cost is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why cost cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 6: Latency

Consider an enterprise workload in which latency is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why latency cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 7: Llm Application Foundations

Consider an enterprise workload in which LLM application foundations is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why LLM application foundations cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 8: Model Routing

Consider an enterprise workload in which model routing is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why model routing cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 9: Capabilities

Consider an enterprise workload in which capabilities is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why capabilities cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 10: Fallback

Consider an enterprise workload in which fallback is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why fallback cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 11: Cost

Consider an enterprise workload in which cost is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why cost cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 12: Latency

Consider an enterprise workload in which latency is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why latency cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 13: Llm Application Foundations

Consider an enterprise workload in which LLM application foundations is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why LLM application foundations cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 14: Model Routing

Consider an enterprise workload in which model routing is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why model routing cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 15: Capabilities

Consider an enterprise workload in which capabilities is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why capabilities cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 16: Fallback

Consider an enterprise workload in which fallback is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why fallback cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 17: Cost

Consider an enterprise workload in which cost is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why cost cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 18: Latency

Consider an enterprise workload in which latency is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why latency cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 19: Llm Application Foundations

Consider an enterprise workload in which LLM application foundations is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why LLM application foundations cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 20: Model Routing

Consider an enterprise workload in which model routing is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why model routing cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 21: Capabilities

Consider an enterprise workload in which capabilities is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why capabilities cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 22: Fallback

Consider an enterprise workload in which fallback is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why fallback cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 23: Cost

Consider an enterprise workload in which cost is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why cost cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 24: Latency

Consider an enterprise workload in which latency is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why latency cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 25: Llm Application Foundations

Consider an enterprise workload in which LLM application foundations is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why LLM application foundations cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 26: Model Routing

Consider an enterprise workload in which model routing is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why model routing cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 27: Capabilities

Consider an enterprise workload in which capabilities is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why capabilities cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 28: Fallback

Consider an enterprise workload in which fallback is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why fallback cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 29: Cost

Consider an enterprise workload in which cost is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why cost cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 30: Latency

Consider an enterprise workload in which latency is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why latency cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 31: Llm Application Foundations

Consider an enterprise workload in which LLM application foundations is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why LLM application foundations cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 32: Model Routing

Consider an enterprise workload in which model routing is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why model routing cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 33: Capabilities

Consider an enterprise workload in which capabilities is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why capabilities cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.
