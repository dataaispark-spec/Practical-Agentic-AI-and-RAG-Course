# Module 26 — Production Evaluation: Regression + A/B Evaluation System

## Mission

Turn AegisAI evaluation into an engineering release gate. A system is not production-ready because one demo looks good; it must remain good across representative tasks, adversarial cases, versions, tenants and cost/latency constraints.

## Evaluation stack

```text
Dataset / production-safe traces
        ↓
Task cases + expected evidence
        ↓
Retrieval evaluation
        ↓
Generation / citation evaluation
        ↓
Agent trajectory evaluation
        ↓
Security + policy evaluation
        ↓
Cost + latency evaluation
        ↓
Regression / A-B decision
        ↓
Release gate
```

## Learning outcomes

- Build deterministic evaluation cases.
- Separate retrieval, generation, tool, agent and end-to-end metrics.
- Design golden datasets without leakage.
- Compare model/prompt/retrieval versions fairly.
- Use confidence intervals and minimum practical improvements.
- Run A/B and shadow evaluations.
- Detect regressions hidden by averages.
- Evaluate safety and authorization separately from answer quality.
- Convert production incidents into permanent regression tests.

## Evaluation dimensions

### Task success
Did the system accomplish the user's actual goal?

### Retrieval
Recall@K, MRR, nDCG, evidence precision and coverage.

### Generation
Groundedness, citation correctness, completeness and factual consistency.

### Agent behavior
Tool correctness, plan validity, verifier pass rate, unnecessary actions and trajectory efficiency.

### Security
Injection resistance, policy adherence, tenant isolation and unauthorized-action rate.

### Operations
Latency, token use, cost, retries, timeout rate and resource consumption.

## Golden-case contract

Each case should capture:

```text
case_id
input
context/tenant
expected outcome
acceptable answers or assertions
required evidence
forbidden behavior
risk level
budget
metadata/version
```

Avoid storing secrets or sensitive production content in the benchmark repository.

## Fair comparison rules

When comparing systems, hold constant what should not change:

- evaluation cases;
- task definitions;
- retrieval corpus/version where appropriate;
- tool fixtures;
- safety policy;
- budget;
- judge protocol.

Record everything that does change.

## Statistical thinking

A/B results should include:

- sample size;
- mean and median;
- tail latency;
- success rate;
- confidence interval;
- failure categories;
- cost per successful task.

Do not declare victory from a tiny noisy sample or from a single aggregate score.

## Detailed labs

### Lab 1 — Evaluation case schema
Build typed cases with assertions and forbidden behaviors.

### Lab 2 — Golden dataset
Create a small enterprise benchmark with retrieval, generation and tool cases.

### Lab 3 — Retrieval regression
Compare two indexes using Recall@K and nDCG.

### Lab 4 — Generation regression
Compare two prompts/models using groundedness and citation correctness.

### Lab 5 — Agent trajectory scoring
Score tool selection, unnecessary actions, verification and completion.

### Lab 6 — Security benchmark
Inject direct/indirect prompt attacks and measure blocked unauthorized actions.

### Lab 7 — Cost-quality frontier
Plot quality against cost per successful task.

### Lab 8 — A/B evaluation
Run two deterministic fixtures and calculate outcome deltas.

### Lab 9 — Shadow evaluation
Evaluate a candidate version without affecting production users.

### Lab 10 — Regression gate
Fail a release when critical quality or safety metrics cross thresholds.

### Lab 11 — Confidence intervals
Estimate uncertainty and avoid overclaiming small improvements.

### Lab 12 — Incident-to-test
Convert a Module 22 incident into a regression case.

### Lab 13 — Metric gaming
Construct a system that improves one metric while degrading real task success; detect it.

### Lab 14 — Slice analysis
Find failures by tenant, task type, language, risk, retrieval depth or tool path.

### Lab 15 — Release certification
Produce an evaluation report with pass/fail decision and evidence.

## Failure-first exercises

- leaked benchmark answers;
- duplicate cases;
- judge bias;
- tiny sample size;
- cherry-picked successful runs;
- average hides p95 regression;
- quality improves while security degrades;
- cost doubles for a tiny gain;
- candidate changes retrieval and model simultaneously;
- one tenant regresses while global score improves.

## Production release gate

Example policy:

```text
BLOCK if critical security test fails
BLOCK if task success drops beyond tolerance
BLOCK if groundedness drops beyond tolerance
BLOCK if p95 latency violates SLO
BLOCK if cost/success exceeds budget
WARN if small statistically uncertain regression
```

The gate must be explicit, versioned and reviewable.

## Industry scenarios

**Banking:** transaction-assistant evaluation must treat unauthorized actions as catastrophic regardless of answer-quality score.

**Healthcare:** evaluate evidence grounding and unsafe recommendations separately.

**Cybersecurity:** measure correct containment decisions, false positives and policy violations.

**Enterprise IT:** evaluate resolution success, tool correctness, rollback behavior and change-risk constraints.

## Interview bank

1. What makes a good evaluation case?
2. Why separate retrieval from generation evaluation?
3. Why can average quality be misleading?
4. How do you evaluate agent trajectories?
5. How do you prevent benchmark leakage?
6. When is an A/B result statistically meaningful?
7. How do you evaluate safety separately from usefulness?
8. What belongs in a release gate?
9. How do you compare two changing components fairly?
10. How do you turn incidents into regression tests?
11. What is shadow evaluation?
12. How would you evaluate 100,000 agent tasks?

## Coding challenges

- evaluation-case validator;
- metric aggregator;
- Recall/MRR/nDCG calculator;
- trajectory scorer;
- slice analyzer;
- confidence-interval calculator;
- A/B comparator;
- regression gate;
- benchmark leakage detector;
- evaluation report generator.

## Mastery gate

Take two AegisAI versions, run the same benchmark, analyze quality/security/cost/latency slices, quantify uncertainty and produce a defensible release decision.

## Gold challenge

Build **AegisAI Production Evaluation System** connected to Modules 11, 22 and 25. Every production incident can become a benchmark case, every candidate release is evaluated consistently, and critical safety regressions automatically block deployment.
