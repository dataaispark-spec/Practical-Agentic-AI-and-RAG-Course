# Module 5 — Prompting + Evaluation


## Mission
Move prompting from “try wording until it looks good” to an engineering discipline: define task contracts, create representative datasets, run repeatable evaluations, classify failures, and prevent regressions.

## Core principle

> A prompt is a program specification for a probabilistic component; an evaluation harness is how you discover whether the specification is working.

## Learning outcomes

1. Design prompts around explicit task contracts.
2. Separate instructions, context, examples, and policy constraints.
3. Build deterministic test cases around non-deterministic model behavior.
4. Score structured outputs and semantic answers.
5. Distinguish exact-match, rubric, groundedness, and task-success evaluation.
6. Build regression datasets and compare prompt/model versions.
7. Diagnose prompt failures without blindly rewriting prompts.
8. Introduce evaluator disagreement and false-positive analysis.
9. Track latency and cost alongside quality.
10. Explain evaluation methodology in interviews and design reviews.

## Prompt architecture

```text
System policy
     |
Task contract
     |
Few-shot examples (optional)
     |
Retrieved/context data
     |
User input
     |
Output schema
```

Keep stable policy separate from user-controlled content. Delimit untrusted content explicitly.

## Task contract

Every production prompt should define:

```text
Input:
Output:
Allowed behavior:
Forbidden behavior:
Evidence requirements:
Uncertainty behavior:
Failure behavior:
```

For structured output, validate the result in code. Prompt instructions are not a substitute for runtime validation.

## Evaluation ladder

| Level | Technique | Best for |
|---|---|---|
| 1 | syntax/schema checks | structured outputs |
| 2 | exact match | deterministic labels |
| 3 | reference comparison | known answers |
| 4 | rubric evaluator | nuanced quality |
| 5 | pairwise comparison | prompt/model variants |
| 6 | task-success evaluation | real workflow outcomes |
| 7 | production feedback | long-term behavior |

No single metric is sufficient for every AI application.

## Dataset design

A useful evaluation set contains:

- common cases
- edge cases
- adversarial cases
- ambiguous cases
- long-context cases
- multilingual cases when relevant
- policy-sensitive cases
- known historical failures

Do not optimize against a tiny dataset until the prompt memorizes it.

## Lab — Evaluation Harness

Build:

```text
app/
  contracts.py
  prompts.py
  evaluators.py
  runner.py
  report.py

datasets/
  smoke.jsonl
  regression.jsonl

tests/
  test_evaluators.py
  test_runner.py
```

The harness should run a model adapter against a dataset and emit:

```json
{
  "version": "prompt-v3/model-a",
  "cases": 100,
  "passed": 87,
  "task_success_rate": 0.87,
  "schema_pass_rate": 0.98,
  "mean_latency_ms": 920,
  "estimated_cost_usd": 1.42,
  "failure_categories": {
    "missing_evidence": 5,
    "wrong_format": 3,
    "incorrect_reasoning": 5
  }
}
```

## Reference evaluator design

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Case:
    input: str
    expected: str


def exact_match(expected: str, actual: str) -> bool:
    return expected.strip() == actual.strip()
```

Start with deterministic evaluators before adding an LLM judge.

## LLM-as-judge: use carefully

An evaluator model can score nuanced responses, but it introduces another probabilistic component.

Control it with:

- fixed rubric
- structured evaluator output
- calibration examples
- agreement checks
- human spot checks
- evaluator versioning
- judge bias tests

Never treat a judge score as unquestionable ground truth.

## Failure lab

### Failure 1 — “Looks good” evaluation

**Symptom:** the prompt ships because developers manually liked ten examples.

**Fix:** representative regression dataset.

### Failure 2 — Accuracy-only optimization

**Symptom:** answer correctness rises while latency/cost doubles.

**Fix:** multi-objective scorecard.

### Failure 3 — Dataset leakage

**Symptom:** benchmark score is excellent but production performance is poor.

**Fix:** hold out unseen cases and add production-derived failures.

### Failure 4 — Judge drift

**Symptom:** quality score changes after evaluator model/version changes.

**Fix:** version evaluators and maintain calibration cases.

### Failure 5 — Prompt injection in evaluation data

**Symptom:** malicious test content changes evaluator behavior.

**Fix:** isolate candidate output from evaluator instructions and test adversarially.

## Experiment matrix

For every prompt/model change record:

```text
baseline version
candidate version
same dataset
quality delta
latency delta
cost delta
failure-category delta
statistical/decision threshold
promotion decision
```

## Industry challenge

A support classifier has:

- 92% overall accuracy
- 70% accuracy on rare high-severity incidents
- 40% lower latency than the stronger model

Should it ship? Define the evaluation slice and business risk before answering.

## Interview bank

1. Why is prompting an engineering problem?
2. What is a task contract?
3. How do you build a regression dataset?
4. When is exact match appropriate?
5. What is pairwise evaluation?
6. What are weaknesses of LLM-as-judge?
7. How do you prevent evaluator drift?
8. Why evaluate latency and cost with quality?
9. What is dataset leakage?
10. How do you test prompt injection?
11. How would you compare two prompts fairly?
12. How do you choose a promotion threshold?
13. How do you classify failures?
14. What is task success?
15. How do you evaluate structured output?
16. How would you evaluate a chatbot with no single correct answer?
17. How do you combine automated and human evaluation?
18. How would you detect benchmark gaming?
19. How do you version evaluation datasets?
20. Design an evaluation system for a production RAG assistant.

## Mastery gate

You can advance when you can build an evaluation harness that compares versions on a fixed regression set, reports quality/cost/latency, classifies failures, and blocks a regression automatically.

## Expanded long-form course chapter

This course is a practical engineering progression from deterministic software and LLM applications to retrieval, tools, stateful agents, distributed coordination, knowledge graphs, durable autonomy, verification, computer use, and controlled self-improvement. The governing idea is that an AI system becomes production-grade not by adding more model calls, but by adding explicit boundaries around probabilistic decisions. Throughout the 43 modules, the learner repeatedly asks: What is the goal? What state is authoritative? What evidence is available? What actions are permitted? What budget applies? What must be verified? What happens when a dependency fails? What must be observable and auditable? What evidence would justify changing the design?

The course uses the AegisAI mental model: Model + Harness + Environment + Tools + State + Policy + Budget + Verification. Retrieval is treated as a knowledge mechanism; an agent loop is treated as a decision-and-action mechanism; a harness is treated as the control plane around the model; and a verifier is treated as an independent check on outcomes. This distinction prevents a common engineering failure in which a prompt is asked to perform authorization, correctness checking, persistence, and business policy simultaneously.

Every module follows the same learning rhythm: Predict → Run → Observe → Explain → Break → Debug → Measure → Improve → Defend. The examples therefore emphasize observable mechanisms, explicit contracts, failure injection, metrics, and regression tests. The notebooks and applications are intended to work with deterministic fakes and synthetic data wherever possible, so that the learner can understand the mechanism before depending on a commercial provider.

## Module-specific learning contract

This expanded chapter deepens the repository canonical learning objectives for **Module 5: Prompting + Evaluation**. The objective vocabulary is preserved: prompting, evaluation, task contract, regression, and judge calibration. Each concept is connected to architecture, implementation, failure analysis, evaluation, security, operations and system-design reasoning.

## First-principles concepts

### 1. Prompting

The first principle for Prompting + Evaluation is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, prompting should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Evaluation

A practical way to learn Prompting + Evaluation is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for evaluation; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Task Contract

In an enterprise setting, Prompting + Evaluation rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. task contract becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Regression

The failure-first perspective is especially important for Prompting + Evaluation. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For regression, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Judge Calibration

Measurement should accompany every meaningful change to Prompting + Evaluation. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For judge calibration, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Prompting

A useful architecture diagram for Prompting + Evaluation separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For prompting, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Evaluation

Versioning is part of the technical design of Prompting + Evaluation, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If evaluation changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Task Contract

The final production question for Prompting + Evaluation is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For task contract, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Architecture and control boundaries

### 1. Prompting

The first principle for Prompting + Evaluation is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, prompting should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Evaluation

A practical way to learn Prompting + Evaluation is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for evaluation; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Task Contract

In an enterprise setting, Prompting + Evaluation rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. task contract becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Regression

The failure-first perspective is especially important for Prompting + Evaluation. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For regression, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Judge Calibration

Measurement should accompany every meaningful change to Prompting + Evaluation. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For judge calibration, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Prompting

A useful architecture diagram for Prompting + Evaluation separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For prompting, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Evaluation

Versioning is part of the technical design of Prompting + Evaluation, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If evaluation changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Task Contract

The final production question for Prompting + Evaluation is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For task contract, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Mechanisms and implementation reasoning

### 1. Prompting

The first principle for Prompting + Evaluation is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, prompting should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Evaluation

A practical way to learn Prompting + Evaluation is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for evaluation; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Task Contract

In an enterprise setting, Prompting + Evaluation rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. task contract becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Regression

The failure-first perspective is especially important for Prompting + Evaluation. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For regression, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Judge Calibration

Measurement should accompany every meaningful change to Prompting + Evaluation. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For judge calibration, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Prompting

A useful architecture diagram for Prompting + Evaluation separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For prompting, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Evaluation

Versioning is part of the technical design of Prompting + Evaluation, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If evaluation changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Task Contract

The final production question for Prompting + Evaluation is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For task contract, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Industry scenarios and worked examples

### 1. Prompting

The first principle for Prompting + Evaluation is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, prompting should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Evaluation

A practical way to learn Prompting + Evaluation is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for evaluation; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Task Contract

In an enterprise setting, Prompting + Evaluation rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. task contract becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Regression

The failure-first perspective is especially important for Prompting + Evaluation. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For regression, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Judge Calibration

Measurement should accompany every meaningful change to Prompting + Evaluation. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For judge calibration, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Prompting

A useful architecture diagram for Prompting + Evaluation separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For prompting, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Evaluation

Versioning is part of the technical design of Prompting + Evaluation, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If evaluation changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Task Contract

The final production question for Prompting + Evaluation is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For task contract, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Failure-first engineering

### 1. Prompting

The first principle for Prompting + Evaluation is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, prompting should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Evaluation

A practical way to learn Prompting + Evaluation is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for evaluation; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Task Contract

In an enterprise setting, Prompting + Evaluation rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. task contract becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Regression

The failure-first perspective is especially important for Prompting + Evaluation. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For regression, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Judge Calibration

Measurement should accompany every meaningful change to Prompting + Evaluation. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For judge calibration, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Prompting

A useful architecture diagram for Prompting + Evaluation separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For prompting, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Evaluation

Versioning is part of the technical design of Prompting + Evaluation, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If evaluation changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Task Contract

The final production question for Prompting + Evaluation is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For task contract, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Experiments and measurement

### 1. Prompting

The first principle for Prompting + Evaluation is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, prompting should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Evaluation

A practical way to learn Prompting + Evaluation is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for evaluation; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Task Contract

In an enterprise setting, Prompting + Evaluation rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. task contract becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Regression

The failure-first perspective is especially important for Prompting + Evaluation. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For regression, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Judge Calibration

Measurement should accompany every meaningful change to Prompting + Evaluation. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For judge calibration, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Prompting

A useful architecture diagram for Prompting + Evaluation separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For prompting, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Evaluation

Versioning is part of the technical design of Prompting + Evaluation, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If evaluation changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Task Contract

The final production question for Prompting + Evaluation is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For task contract, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Security, governance and responsible operation

### 1. Prompting

The first principle for Prompting + Evaluation is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, prompting should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Evaluation

A practical way to learn Prompting + Evaluation is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for evaluation; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Task Contract

In an enterprise setting, Prompting + Evaluation rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. task contract becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Regression

The failure-first perspective is especially important for Prompting + Evaluation. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For regression, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Judge Calibration

Measurement should accompany every meaningful change to Prompting + Evaluation. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For judge calibration, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Prompting

A useful architecture diagram for Prompting + Evaluation separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For prompting, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Evaluation

Versioning is part of the technical design of Prompting + Evaluation, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If evaluation changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Task Contract

The final production question for Prompting + Evaluation is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For task contract, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Production design and operational readiness

### 1. Prompting

The first principle for Prompting + Evaluation is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, prompting should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Evaluation

A practical way to learn Prompting + Evaluation is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for evaluation; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Task Contract

In an enterprise setting, Prompting + Evaluation rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. task contract becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Regression

The failure-first perspective is especially important for Prompting + Evaluation. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For regression, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Judge Calibration

Measurement should accompany every meaningful change to Prompting + Evaluation. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For judge calibration, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Prompting

A useful architecture diagram for Prompting + Evaluation separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For prompting, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Evaluation

Versioning is part of the technical design of Prompting + Evaluation, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If evaluation changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Task Contract

The final production question for Prompting + Evaluation is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For task contract, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Debugging and incident analysis

### 1. Prompting

The first principle for Prompting + Evaluation is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, prompting should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Evaluation

A practical way to learn Prompting + Evaluation is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for evaluation; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Task Contract

In an enterprise setting, Prompting + Evaluation rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. task contract becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Regression

The failure-first perspective is especially important for Prompting + Evaluation. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For regression, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Judge Calibration

Measurement should accompany every meaningful change to Prompting + Evaluation. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For judge calibration, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Prompting

A useful architecture diagram for Prompting + Evaluation separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For prompting, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Evaluation

Versioning is part of the technical design of Prompting + Evaluation, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If evaluation changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Task Contract

The final production question for Prompting + Evaluation is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For task contract, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Exercises and independent practice

### 1. Prompting

The first principle for Prompting + Evaluation is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, prompting should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Evaluation

A practical way to learn Prompting + Evaluation is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for evaluation; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Task Contract

In an enterprise setting, Prompting + Evaluation rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. task contract becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Regression

The failure-first perspective is especially important for Prompting + Evaluation. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For regression, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Judge Calibration

Measurement should accompany every meaningful change to Prompting + Evaluation. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For judge calibration, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Prompting

A useful architecture diagram for Prompting + Evaluation separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For prompting, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Evaluation

Versioning is part of the technical design of Prompting + Evaluation, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If evaluation changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Task Contract

The final production question for Prompting + Evaluation is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For task contract, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## System-design review

### 1. Prompting

The first principle for Prompting + Evaluation is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, prompting should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Evaluation

A practical way to learn Prompting + Evaluation is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for evaluation; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Task Contract

In an enterprise setting, Prompting + Evaluation rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. task contract becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Regression

The failure-first perspective is especially important for Prompting + Evaluation. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For regression, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Judge Calibration

Measurement should accompany every meaningful change to Prompting + Evaluation. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For judge calibration, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Prompting

A useful architecture diagram for Prompting + Evaluation separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For prompting, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Evaluation

Versioning is part of the technical design of Prompting + Evaluation, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If evaluation changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Task Contract

The final production question for Prompting + Evaluation is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For task contract, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Assessment and mastery

### Question 1

Explain how you would design, implement, test, observe and defend **prompting** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 2

Explain how you would design, implement, test, observe and defend **evaluation** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 3

Explain how you would design, implement, test, observe and defend **task contract** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 4

Explain how you would design, implement, test, observe and defend **regression** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 5

Explain how you would design, implement, test, observe and defend **judge calibration** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 6

Explain how you would design, implement, test, observe and defend **prompting** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 7

Explain how you would design, implement, test, observe and defend **evaluation** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 8

Explain how you would design, implement, test, observe and defend **task contract** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 9

Explain how you would design, implement, test, observe and defend **regression** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 10

Explain how you would design, implement, test, observe and defend **judge calibration** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 11

Explain how you would design, implement, test, observe and defend **prompting** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 12

Explain how you would design, implement, test, observe and defend **evaluation** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 13

Explain how you would design, implement, test, observe and defend **task contract** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 14

Explain how you would design, implement, test, observe and defend **regression** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 15

Explain how you would design, implement, test, observe and defend **judge calibration** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 16

Explain how you would design, implement, test, observe and defend **prompting** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 17

Explain how you would design, implement, test, observe and defend **evaluation** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 18

Explain how you would design, implement, test, observe and defend **task contract** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 19

Explain how you would design, implement, test, observe and defend **regression** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 20

Explain how you would design, implement, test, observe and defend **judge calibration** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 21

Explain how you would design, implement, test, observe and defend **prompting** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 22

Explain how you would design, implement, test, observe and defend **evaluation** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 23

Explain how you would design, implement, test, observe and defend **task contract** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 24

Explain how you would design, implement, test, observe and defend **regression** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 25

Explain how you would design, implement, test, observe and defend **judge calibration** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 26

Explain how you would design, implement, test, observe and defend **prompting** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 27

Explain how you would design, implement, test, observe and defend **evaluation** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 28

Explain how you would design, implement, test, observe and defend **task contract** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 29

Explain how you would design, implement, test, observe and defend **regression** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 30

Explain how you would design, implement, test, observe and defend **judge calibration** in a real Prompting + Evaluation system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

## Mastery gate

Completion means being able to explain the mechanism from first principles, implement the smallest working version, deliberately break it, identify the first failing boundary from evidence, repair it, measure the repaired system against a baseline, and defend the resulting trade-offs. The learner should also explain when not to use the mechanism. Production expertise includes recognizing when a simpler deterministic solution is safer, cheaper and easier to operate.

## Deep case study 1: Prompting

Consider an enterprise workload in which prompting is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why prompting cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 2: Evaluation

Consider an enterprise workload in which evaluation is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why evaluation cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 3: Task Contract

Consider an enterprise workload in which task contract is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why task contract cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 4: Regression

Consider an enterprise workload in which regression is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why regression cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 5: Judge Calibration

Consider an enterprise workload in which judge calibration is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why judge calibration cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 6: Prompting

Consider an enterprise workload in which prompting is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why prompting cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 7: Evaluation

Consider an enterprise workload in which evaluation is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why evaluation cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 8: Task Contract

Consider an enterprise workload in which task contract is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why task contract cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 9: Regression

Consider an enterprise workload in which regression is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why regression cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 10: Judge Calibration

Consider an enterprise workload in which judge calibration is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why judge calibration cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 11: Prompting

Consider an enterprise workload in which prompting is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why prompting cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 12: Evaluation

Consider an enterprise workload in which evaluation is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why evaluation cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 13: Task Contract

Consider an enterprise workload in which task contract is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why task contract cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 14: Regression

Consider an enterprise workload in which regression is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why regression cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 15: Judge Calibration

Consider an enterprise workload in which judge calibration is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why judge calibration cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 16: Prompting

Consider an enterprise workload in which prompting is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why prompting cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 17: Evaluation

Consider an enterprise workload in which evaluation is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why evaluation cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 18: Task Contract

Consider an enterprise workload in which task contract is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why task contract cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 19: Regression

Consider an enterprise workload in which regression is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why regression cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 20: Judge Calibration

Consider an enterprise workload in which judge calibration is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why judge calibration cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 21: Prompting

Consider an enterprise workload in which prompting is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why prompting cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 22: Evaluation

Consider an enterprise workload in which evaluation is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why evaluation cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 23: Task Contract

Consider an enterprise workload in which task contract is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why task contract cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 24: Regression

Consider an enterprise workload in which regression is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why regression cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 25: Judge Calibration

Consider an enterprise workload in which judge calibration is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why judge calibration cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 26: Prompting

Consider an enterprise workload in which prompting is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why prompting cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 27: Evaluation

Consider an enterprise workload in which evaluation is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why evaluation cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 28: Task Contract

Consider an enterprise workload in which task contract is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why task contract cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 29: Regression

Consider an enterprise workload in which regression is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why regression cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 30: Judge Calibration

Consider an enterprise workload in which judge calibration is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why judge calibration cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 31: Prompting

Consider an enterprise workload in which prompting is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why prompting cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 32: Evaluation

Consider an enterprise workload in which evaluation is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why evaluation cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 33: Task Contract

Consider an enterprise workload in which task contract is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why task contract cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 34: Regression

Consider an enterprise workload in which regression is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why regression cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.
