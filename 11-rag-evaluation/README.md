# Module 11 — RAG Evaluation Engineering

## Mission
Build an evaluation system that tells you **whether retrieval and generation actually improved**, instead of relying on demos or subjective inspection.

## Evaluation stack
```text
Dataset → Retrieval evaluation → Evidence evaluation → Answer evaluation
              ↓                       ↓                    ↓
         Recall/MRR/nDCG       groundedness/coverage   correctness/relevance
                                      ↓
                              regression + experiment report
```

## Learning outcomes
You will build:
- a versioned golden dataset;
- retrieval metrics and answer metrics;
- deterministic evaluators where possible;
- calibrated model-assisted judges;
- failure classification;
- regression gates;
- experiment comparisons;
- production evaluation telemetry.

## What must be evaluated separately
1. **Retrieval:** Did we retrieve the right evidence?
2. **Evidence quality:** Is the evidence sufficient and non-conflicting?
3. **Generation:** Is the answer correct and grounded in that evidence?
4. **Task success:** Did the complete application accomplish the user's objective?

A good answer does not prove good retrieval, and good retrieval does not prove a good answer.

## Dataset design
Each case should contain:
- case ID;
- tenant/security context;
- user query;
- expected document/chunk IDs;
- expected answer or answer rubric;
- answerability flag;
- difficulty/query class;
- prohibited claims if relevant;
- dataset version.

Include positive, negative, ambiguous, unanswerable, stale-information and adversarial cases.

## Metrics
### Retrieval
- Recall@K
- Precision@K
- MRR
- nDCG@K
- candidate count

### Generation
- exact match where appropriate;
- semantic correctness;
- groundedness/faithfulness;
- citation correctness;
- completeness;
- refusal/abstention correctness.

### System
- task success;
- p50/p95 latency;
- tokens;
- cost/request;
- tool errors;
- security violations.

## Lab 1 — Golden dataset
Create 50 enterprise queries across five query classes. Label relevant documents and expected answers. Add at least 10 unanswerable cases.

## Lab 2 — Retrieval benchmark
Run Modules 6–10 retrieval variants. Produce Recall@1/5/10, MRR and nDCG tables.

## Lab 3 — Groundedness evaluator
For each generated claim, determine whether supporting evidence exists. Start with a deterministic citation/evidence checker before adding an LLM judge.

## Lab 4 — Judge calibration
Create 30 examples labeled by humans. Compare the evaluator's judgments. Calculate agreement, false positives and false negatives. Inspect disagreements instead of hiding them in one aggregate score.

## Lab 5 — Regression gate
Create baseline results. Fail the evaluation when a new version drops below configured quality thresholds without an approved exception.

## Lab 6 — Slice analysis
Break results down by query type, tenant, document type, difficulty and answerability. Find regressions hidden by aggregate averages.

## Lab 7 — Adversarial evaluation
Add prompt injection, conflicting documents, stale documents, irrelevant top-K evidence and malicious citations. Verify that safety and grounding metrics remain within limits.

## Lab 8 — Experiment runner
Compare two retrieval configurations and automatically generate a report containing metrics, deltas, failures and a promotion recommendation.

## Detailed exercises
1. Build 100 labeled queries.
2. Define a retrieval quality SLO.
3. Define an answer correctness rubric.
4. Implement Recall@K and MRR from scratch.
5. Add citation correctness scoring.
6. Build an evaluator disagreement report.
7. Create a regression threshold with minimum sample requirements.
8. Add bootstrap confidence intervals to compare two versions.
9. Detect Simpson's-paradox-style aggregate improvements using slices.
10. Create a promotion rule requiring quality + latency + security constraints simultaneously.
11. Test whether an LLM judge is biased toward longer answers.
12. Test evaluator stability by changing irrelevant formatting.

## Failure-first exercises
- **Metric gaming:** optimize only one metric and observe degradation elsewhere.
- **Judge drift:** change judge prompt/model and compare scores.
- **Dataset leakage:** put evaluation answers into retrieval corpus and detect inflated performance.
- **Aggregate masking:** hide a tenant-specific regression inside a high overall score.
- **Unanswerable failure:** reward hallucinated answers accidentally.
- **Citation theater:** count citations without verifying that they support claims.

## Production evaluation architecture
```text
Offline datasets ──→ Evaluation Runner ──→ Metrics Store
                         │                    ↓
                         ├──────────────→ Dashboard
                         ↓
                   Regression Gate
                         ↓
                   CI/CD promotion

Online traces ───────────────→ Sampling ──→ Human review
                                      └──→ continuous evaluation set
```

## Security
Evaluation data can contain sensitive information. Maintain dataset access controls, tenant separation, redaction and provenance. Never treat an LLM judge as the sole security control.

## Interview questions
1. Why separate retrieval and generation evaluation?
2. When is exact match useful?
3. Explain MRR.
4. Explain nDCG.
5. What makes a good golden dataset?
6. How do you evaluate unanswerable questions?
7. What are weaknesses of LLM-as-a-judge?
8. How do you calibrate a judge?
9. How do you detect dataset leakage?
10. How do you design regression gates?
11. Why use slice analysis?
12. How do you compare two systems statistically?
13. How do you evaluate citation correctness?
14. How do you measure groundedness?
15. How do you prevent metric gaming?

## System-design challenge
Design an evaluation platform for 20 RAG configurations, 10,000 golden cases, multiple tenants and daily production sampling. It must support reproducible runs, evaluator versioning, regression gates, human review and auditability.

## Mastery gate
You pass when you can create a trustworthy benchmark, diagnose metric disagreements, calibrate judges, detect regressions, and defend why a new RAG version should or should not ship.

## Google Colab
`notebooks/module_11_rag_evaluation.ipynb` is self-contained and demonstrates dataset creation, retrieval metrics, answer scoring, evaluator calibration, slice analysis and regression gates.
