# Module 12 — RAG Debugging & Failure Investigation Lab

## Mission
Learn to debug RAG as an observable distributed pipeline instead of blaming the LLM.

## Debugging model
```text
User query
  ↓
query normalization
  ↓
retrieval
  ↓
filtering
  ↓
ranking/reranking
  ↓
evidence assembly
  ↓
prompt construction
  ↓
LLM generation
  ↓
citations / abstention
```

Every stage must emit structured evidence about what happened.

## Failure taxonomy
### Retrieval failures
- query mismatch;
- bad chunking;
- missing document;
- stale index;
- wrong embedding model/version;
- bad metadata filter;
- candidate truncation.

### Ranking failures
- lexical bias;
- semantic false positives;
- poor fusion;
- reranker error;
- duplicate evidence.

### Generation failures
- unsupported claim;
- evidence ignored;
- conflicting evidence mishandled;
- hallucination;
- citation mismatch;
- incorrect abstention.

### System failures
- timeout;
- provider error;
- cache corruption;
- configuration mismatch;
- authorization failure.

## Trace contract
Each request should record:
- request/run ID;
- tenant/principal;
- query;
- query transformation;
- retriever configuration;
- candidate IDs and scores;
- filters applied;
- reranker scores;
- final evidence IDs;
- prompt hash/version;
- model/provider/version;
- output;
- citations;
- latency by stage;
- token/cost counters;
- policy decisions;
- errors/retries.

Do not log sensitive content unnecessarily. Prefer IDs, hashes and controlled evidence previews.

## Detailed labs
### Lab 1 — Golden trace reconstruction
Given a failed answer, reconstruct the complete retrieval path and identify the first incorrect stage.

### Lab 2 — Retrieval failure
Inject an irrelevant embedding result. Determine whether query, chunking or embedding caused the problem.

### Lab 3 — Filter failure
Break tenant filtering and build a test that detects unauthorized candidates before generation.

### Lab 4 — Ranking failure
Return a correct document at rank 20 and restrict candidate K to 5. Prove the reranker cannot fix candidate-generation loss.

### Lab 5 — Generation failure
Provide correct evidence but an incorrect generated claim. Determine whether prompt construction, model behavior or evidence formatting is responsible.

### Lab 6 — Conflicting evidence
Create two versioned documents with contradictory policy statements. Build conflict detection and require explicit version handling.

### Lab 7 — Stale index
Update a document without re-indexing. Detect freshness mismatch from provenance metadata.

### Lab 8 — Latency investigation
Inject slow stages and use stage-level timing to locate p95 regression.

### Lab 9 — Cost investigation
Find unnecessary retrieval expansion and oversized contexts. Calculate avoidable token cost.

### Lab 10 — Incident report
Turn a failing trace into a production incident report containing impact, root cause, contributing factors, mitigation, regression test and permanent fix.

## Exercises
1. Build a structured trace schema.
2. Write a trace-to-root-cause classifier.
3. Add first-failure detection.
4. Create five synthetic incidents.
5. Build regression tests for each incident.
6. Detect stale index versions automatically.
7. Detect duplicate evidence.
8. Detect citation/evidence mismatch.
9. Add stage-level latency budgets.
10. Create a “do not blame the LLM first” debugging checklist.

## Failure-first challenge
Start with a deliberately broken RAG system and diagnose seven failures without reading the implementation. You may inspect only traces, metrics and outputs. Then inspect the code and compare your hypothesis with reality.

## Production architecture
```text
Request
 ↓
Trace context
 ↓
RAG pipeline ──→ structured spans ──→ telemetry store
 ↓                                  ↓
Evidence ledger                 dashboards/alerts
 ↓                                  ↓
Answer                          incident investigation
```

## Security
Debug logs can become a data-exfiltration path. Redact or tokenize PII, restrict trace access, isolate tenants and avoid storing complete prompts/responses by default when unnecessary.

## Interview questions
1. How do you distinguish retrieval from generation failure?
2. What is the first artifact you inspect?
3. Why is traceability essential in RAG?
4. How do you diagnose stale knowledge?
5. How do you diagnose a reranker problem?
6. How do you detect citation mismatch?
7. How do you debug p95 latency?
8. How do you debug cost spikes?
9. What belongs in a RAG trace?
10. How do you avoid leaking sensitive data through logs?

## System-design challenge
Design a RAG observability/debugging platform supporting 10,000 QPS, sampling, tenant isolation, trace retention policies, replayable evaluations and incident investigation.

## Mastery gate
You pass when you can take an unexplained bad answer, reconstruct the pipeline, identify the first failing stage, prove the root cause with evidence, implement a regression test and demonstrate that the fix works.

## Google Colab
`notebooks/module_12_rag_debugging.ipynb` contains synthetic broken pipelines, trace inspection, failure classification, stage-latency analysis and incident exercises.
