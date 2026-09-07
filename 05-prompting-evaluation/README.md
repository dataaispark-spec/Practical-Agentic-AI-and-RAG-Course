# Module 5 — Prompting + Evaluation: Build an LLM Evaluation Harness

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
