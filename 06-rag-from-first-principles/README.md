# Module 6 — RAG From First Principles



## Mission
Build retrieval-augmented generation without hiding the important mechanics behind a framework. You will implement a small RAG engine from raw text through chunking, vector representation, similarity search, evidence selection, prompt assembly, and grounded answer generation.

## Learning outcomes

You will be able to:

1. Explain why parametric model knowledge is insufficient for changing/private information.
2. Design chunking and metadata strategies.
3. Understand embeddings as vectors rather than magic search tokens.
4. Implement similarity search from first principles.
5. Separate retrieval quality from generation quality.
6. Inspect retrieved evidence and diagnose failures.
7. Add citations and abstention behavior.
8. Measure Recall@K, MRR, latency and cost.
9. Explain when RAG is worse than long context or a deterministic database query.
10. Design a production RAG architecture with authorization and observability.

## The RAG pipeline

```text
Documents
   |
   v
Normalize / parse
   |
   v
Chunk + metadata
   |
   v
Embedding
   |
   v
Vector index
   |
   v
Query embedding
   |
   v
Similarity search
   |
   v
Top-K evidence
   |
   v
Prompt/context assembly
   |
   v
LLM
   |
   v
Grounded answer + citations / abstention
```

## 1. What RAG actually solves

RAG is a runtime knowledge architecture. It does not magically make a model truthful.

The model still generates the answer; retrieval supplies evidence that the application can inspect and constrain.

Use RAG when information is:

- private
- current or frequently changing
- too large to place into every prompt
- naturally represented as searchable documents

Do not use RAG merely because a project is called an AI assistant. A deterministic database query is usually preferable for exact transactional facts.

## 2. First-principles vector search

Represent a document chunk as a vector:

```text
chunk -> [0.12, -0.44, 0.91, ...]
```

Represent the query similarly:

```text
query -> [0.08, -0.40, 0.87, ...]
```

A common similarity measure is cosine similarity:

```text
cos(q, d) = (q · d) / (||q|| ||d||)
```

The implementation is simple enough to build with Python/NumPy. The hard production problems are usually elsewhere: ingestion quality, chunk boundaries, metadata filtering, authorization, freshness, ranking, evaluation and operations.

## 3. Chunking is information architecture

Bad chunking can destroy retrieval before the model ever sees the data.

Compare:

```text
Document
  -> arbitrary 500-character slices
```

with:

```text
Document
  -> section
      -> subsection
          -> coherent chunk
              + document_id
              + version
              + tenant
              + source
              + effective_date
```

Start with structure-aware chunks when possible. Use overlap only when it addresses a real boundary problem; excessive overlap increases index size and duplicate evidence.

## 4. Metadata is part of retrieval

A production chunk should carry enough metadata for filtering and citation:

```json
{
  "chunk_id": "policy-42-v3-c07",
  "document_id": "policy-42",
  "version": "3",
  "tenant_id": "tenant-a",
  "source": "hr-policy.pdf",
  "section": "Leave",
  "effective_date": "2026-07-01"
}
```

Important: **retrieval correctness is not authorization**. Authorization should be enforced before or during retrieval using deterministic identity and entitlement controls.

## 5. Minimal RAG engine

Build these components without a framework:

```text
Document
Chunker
EmbeddingModel
VectorIndex
Retriever
ContextBuilder
Generator
RAGPipeline
```

Recommended interface:

```python
class Retriever(Protocol):
    def search(self, query: str, top_k: int = 5) -> list[Chunk]: ...
```

The first implementation may use deterministic toy embeddings so the tests do not depend on an external provider.

## 6. Retrieval vs generation

Keep the stages observable:

```text
Query
 |
 +--> retrieved chunks
 |
 +--> ranking scores
 |
 +--> selected evidence
 |
 +--> generated answer
```

If the answer is wrong, ask first:

1. Was the right evidence retrieved?
2. Was it ranked highly enough?
3. Was it actually passed to the model?
4. Did the model use the evidence correctly?

Without these boundaries, teams often “fix the prompt” for a retrieval problem.

## 7. Grounding and abstention

A robust RAG application should support:

```text
Evidence sufficient?
   |
   +-- yes --> answer using evidence
   |
   +-- no --> abstain / request clarification / route elsewhere
```

Do not manufacture confidence when evidence is missing.

For high-risk domains, require citations or evidence IDs and validate that cited evidence belongs to the authorized retrieval set.

## 8. Evaluation

### Retrieval metrics

**Recall@K:** whether a known relevant document/chunk appears in the top K.

**MRR:** how high the first relevant result appears.

Example:

```text
Query Q1 -> relevant chunk ranked #1 -> reciprocal rank 1.0
Query Q2 -> relevant chunk ranked #4 -> reciprocal rank 0.25
```

### Generation metrics

Evaluate separately:

- groundedness / faithfulness
- answer correctness
- citation correctness
- abstention correctness
- task success

Then add operational metrics:

- retrieval latency
- generation latency
- p95/p99 latency
- token usage
- cost/task

## 9. Hands-on lab — NumPy RAG Engine

Create:

```text
06-rag-from-first-principles/
├── app/
│   ├── models.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── index.py
│   ├── retriever.py
│   ├── prompt.py
│   └── pipeline.py
├── datasets/
│   ├── documents.jsonl
│   └── queries.jsonl
├── tests/
│   ├── test_chunker.py
│   ├── test_index.py
│   └── test_retrieval.py
└── docs/
    └── FAILURE-LAB.md
```

### Build order

1. Define document/chunk contracts.
2. Implement structure-aware chunking.
3. Add deterministic toy embeddings.
4. Implement cosine similarity.
5. Build top-K index search.
6. Add metadata filters.
7. Create retrieval evaluation cases.
8. Add a context builder.
9. Add a fake generator.
10. Inspect every retrieval trace.

## 10. Failure lab

### Failure A — Giant chunks

**Symptom:** relevant information exists but retrieval returns broad, noisy passages.

**Experiment:** compare chunk sizes while holding the embedding model and dataset constant.

### Failure B — Tiny chunks

**Symptom:** retrieved fragments lack the context required to answer.

**Fix:** structure-aware boundaries and measured overlap.

### Failure C — Semantic miss

**Symptom:** keyword-equivalent queries retrieve unrelated chunks.

**Fix path:** inspect embeddings, add hybrid retrieval in Module 9, and create representative query variants.

### Failure D — Stale information

**Symptom:** old policy wins over current policy.

**Fix:** metadata filters/version awareness and freshness tests.

### Failure E — Cross-tenant retrieval

**Symptom:** retrieval finds a relevant chunk belonging to another tenant.

**Lesson:** tenant authorization must be deterministic and testable.

### Failure F — Correct retrieval, wrong answer

**Symptom:** evidence is clearly relevant but the answer contradicts it.

**Diagnosis:** generation/grounding failure, not necessarily retrieval failure.

## 11. Production architecture

```text
                Identity / Policy
                       |
                       v
User -> Query -> Retrieval Gateway
                    |
          +---------+---------+
          |                   |
      metadata filter     vector search
          |                   |
          +---------+---------+
                    |
                    v
               rerank/evidence
                    |
                    v
              Context Builder
                    |
                    v
                  Model
                    |
          +---------+---------+
          |                   |
       validator          citations
          |                   |
          +---------+---------+
                    v
                 Answer
```

For large systems, the vector index becomes an infrastructure service, but the conceptual boundaries remain the same.

## 12. Architecture trade-offs

| Choice | Advantage | Risk |
|---|---|---|
| Long context | simple pipeline | context cost/noise |
| Vector retrieval | scalable semantic search | embedding/retrieval errors |
| Keyword retrieval | exact terminology | weaker semantic matching |
| Hybrid retrieval | complementary signals | more tuning |
| RAG | current/private evidence | ingestion + retrieval complexity |
| Fine-tuning | behavior/style adaptation | poor fit for frequently changing facts |

## 13. Interview bank

1. Explain RAG from first principles.
2. Why does chunking matter?
3. What is cosine similarity?
4. What is Recall@K?
5. What is MRR?
6. Why can high Recall@K still yield bad answers?
7. When would you choose a database query instead of RAG?
8. How do you handle document versioning?
9. How do you enforce tenant isolation?
10. How do you prevent stale chunks from winning?
11. How do you decide chunk size?
12. What is hybrid retrieval?
13. Why can overlap increase cost without improving quality?
14. How do you diagnose retrieval vs generation failure?
15. How would you evaluate citations?
16. How would you implement abstention?
17. How do you handle a 50-million-document corpus?
18. What metadata belongs on a chunk?
19. How would you reduce RAG latency?
20. Design a multi-tenant enterprise RAG system.

## Mastery gate

You can advance when you can build a working RAG pipeline from raw documents to top-K evidence, explain every retrieval score, measure retrieval quality, detect stale/unauthorized evidence, and demonstrate why a failure belongs to ingestion, retrieval, context assembly, or generation.

### Gold challenge

Given 100 documents and 30 labeled questions:

- achieve measurable Recall@5
- produce evidence IDs for every answer
- abstain when evidence is insufficient
- enforce tenant filters
- benchmark at least three chunking strategies
- report latency and cost
- create five deliberate failure cases and diagnose each one.

## Expanded long-form course chapter

This course is a practical engineering progression from deterministic software and LLM applications to retrieval, tools, stateful agents, distributed coordination, knowledge graphs, durable autonomy, verification, computer use, and controlled self-improvement. The governing idea is that an AI system becomes production-grade not by adding more model calls, but by adding explicit boundaries around probabilistic decisions. Throughout the 43 modules, the learner repeatedly asks: What is the goal? What state is authoritative? What evidence is available? What actions are permitted? What budget applies? What must be verified? What happens when a dependency fails? What must be observable and auditable? What evidence would justify changing the design?

The course uses the AegisAI mental model: Model + Harness + Environment + Tools + State + Policy + Budget + Verification. Retrieval is treated as a knowledge mechanism; an agent loop is treated as a decision-and-action mechanism; a harness is treated as the control plane around the model; and a verifier is treated as an independent check on outcomes. This distinction prevents a common engineering failure in which a prompt is asked to perform authorization, correctness checking, persistence, and business policy simultaneously.

Every module follows the same learning rhythm: Predict → Run → Observe → Explain → Break → Debug → Measure → Improve → Defend. The examples therefore emphasize observable mechanisms, explicit contracts, failure injection, metrics, and regression tests. The notebooks and applications are intended to work with deterministic fakes and synthetic data wherever possible, so that the learner can understand the mechanism before depending on a commercial provider.

## Module-specific learning contract

This expanded chapter deepens the repository canonical learning objectives for **Module 6: RAG From First Principles**. The objective vocabulary is preserved: RAG, chunking, embeddings, similarity search, groundedness, and citations. Each concept is connected to architecture, implementation, failure analysis, evaluation, security, operations and system-design reasoning.

## First-principles concepts

### 1. Rag

The first principle for RAG From First Principles is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, RAG should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Chunking

A practical way to learn RAG From First Principles is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for chunking; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Embeddings

In an enterprise setting, RAG From First Principles rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. embeddings becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Similarity Search

The failure-first perspective is especially important for RAG From First Principles. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For similarity search, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Groundedness

Measurement should accompany every meaningful change to RAG From First Principles. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For groundedness, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Citations

A useful architecture diagram for RAG From First Principles separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For citations, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Rag

Versioning is part of the technical design of RAG From First Principles, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If RAG changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Chunking

The final production question for RAG From First Principles is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For chunking, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Architecture and control boundaries

### 1. Rag

The first principle for RAG From First Principles is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, RAG should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Chunking

A practical way to learn RAG From First Principles is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for chunking; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Embeddings

In an enterprise setting, RAG From First Principles rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. embeddings becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Similarity Search

The failure-first perspective is especially important for RAG From First Principles. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For similarity search, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Groundedness

Measurement should accompany every meaningful change to RAG From First Principles. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For groundedness, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Citations

A useful architecture diagram for RAG From First Principles separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For citations, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Rag

Versioning is part of the technical design of RAG From First Principles, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If RAG changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Chunking

The final production question for RAG From First Principles is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For chunking, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Mechanisms and implementation reasoning

### 1. Rag

The first principle for RAG From First Principles is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, RAG should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Chunking

A practical way to learn RAG From First Principles is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for chunking; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Embeddings

In an enterprise setting, RAG From First Principles rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. embeddings becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Similarity Search

The failure-first perspective is especially important for RAG From First Principles. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For similarity search, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Groundedness

Measurement should accompany every meaningful change to RAG From First Principles. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For groundedness, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Citations

A useful architecture diagram for RAG From First Principles separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For citations, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Rag

Versioning is part of the technical design of RAG From First Principles, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If RAG changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Chunking

The final production question for RAG From First Principles is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For chunking, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Industry scenarios and worked examples

### 1. Rag

The first principle for RAG From First Principles is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, RAG should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Chunking

A practical way to learn RAG From First Principles is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for chunking; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Embeddings

In an enterprise setting, RAG From First Principles rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. embeddings becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Similarity Search

The failure-first perspective is especially important for RAG From First Principles. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For similarity search, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Groundedness

Measurement should accompany every meaningful change to RAG From First Principles. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For groundedness, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Citations

A useful architecture diagram for RAG From First Principles separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For citations, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Rag

Versioning is part of the technical design of RAG From First Principles, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If RAG changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Chunking

The final production question for RAG From First Principles is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For chunking, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Failure-first engineering

### 1. Rag

The first principle for RAG From First Principles is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, RAG should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Chunking

A practical way to learn RAG From First Principles is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for chunking; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Embeddings

In an enterprise setting, RAG From First Principles rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. embeddings becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Similarity Search

The failure-first perspective is especially important for RAG From First Principles. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For similarity search, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Groundedness

Measurement should accompany every meaningful change to RAG From First Principles. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For groundedness, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Citations

A useful architecture diagram for RAG From First Principles separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For citations, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Rag

Versioning is part of the technical design of RAG From First Principles, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If RAG changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Chunking

The final production question for RAG From First Principles is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For chunking, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Experiments and measurement

### 1. Rag

The first principle for RAG From First Principles is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, RAG should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Chunking

A practical way to learn RAG From First Principles is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for chunking; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Embeddings

In an enterprise setting, RAG From First Principles rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. embeddings becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Similarity Search

The failure-first perspective is especially important for RAG From First Principles. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For similarity search, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Groundedness

Measurement should accompany every meaningful change to RAG From First Principles. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For groundedness, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Citations

A useful architecture diagram for RAG From First Principles separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For citations, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Rag

Versioning is part of the technical design of RAG From First Principles, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If RAG changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Chunking

The final production question for RAG From First Principles is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For chunking, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Security, governance and responsible operation

### 1. Rag

The first principle for RAG From First Principles is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, RAG should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Chunking

A practical way to learn RAG From First Principles is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for chunking; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Embeddings

In an enterprise setting, RAG From First Principles rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. embeddings becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Similarity Search

The failure-first perspective is especially important for RAG From First Principles. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For similarity search, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Groundedness

Measurement should accompany every meaningful change to RAG From First Principles. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For groundedness, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Citations

A useful architecture diagram for RAG From First Principles separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For citations, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Rag

Versioning is part of the technical design of RAG From First Principles, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If RAG changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Chunking

The final production question for RAG From First Principles is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For chunking, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Production design and operational readiness

### 1. Rag

The first principle for RAG From First Principles is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, RAG should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Chunking

A practical way to learn RAG From First Principles is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for chunking; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Embeddings

In an enterprise setting, RAG From First Principles rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. embeddings becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Similarity Search

The failure-first perspective is especially important for RAG From First Principles. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For similarity search, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Groundedness

Measurement should accompany every meaningful change to RAG From First Principles. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For groundedness, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Citations

A useful architecture diagram for RAG From First Principles separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For citations, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Rag

Versioning is part of the technical design of RAG From First Principles, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If RAG changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Chunking

The final production question for RAG From First Principles is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For chunking, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Debugging and incident analysis

### 1. Rag

The first principle for RAG From First Principles is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, RAG should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Chunking

A practical way to learn RAG From First Principles is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for chunking; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Embeddings

In an enterprise setting, RAG From First Principles rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. embeddings becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Similarity Search

The failure-first perspective is especially important for RAG From First Principles. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For similarity search, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Groundedness

Measurement should accompany every meaningful change to RAG From First Principles. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For groundedness, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Citations

A useful architecture diagram for RAG From First Principles separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For citations, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Rag

Versioning is part of the technical design of RAG From First Principles, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If RAG changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Chunking

The final production question for RAG From First Principles is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For chunking, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Exercises and independent practice

### 1. Rag

The first principle for RAG From First Principles is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, RAG should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Chunking

A practical way to learn RAG From First Principles is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for chunking; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Embeddings

In an enterprise setting, RAG From First Principles rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. embeddings becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Similarity Search

The failure-first perspective is especially important for RAG From First Principles. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For similarity search, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Groundedness

Measurement should accompany every meaningful change to RAG From First Principles. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For groundedness, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Citations

A useful architecture diagram for RAG From First Principles separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For citations, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Rag

Versioning is part of the technical design of RAG From First Principles, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If RAG changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Chunking

The final production question for RAG From First Principles is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For chunking, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## System-design review

### 1. Rag

The first principle for RAG From First Principles is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, RAG should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Chunking

A practical way to learn RAG From First Principles is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for chunking; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Embeddings

In an enterprise setting, RAG From First Principles rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. embeddings becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Similarity Search

The failure-first perspective is especially important for RAG From First Principles. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For similarity search, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Groundedness

Measurement should accompany every meaningful change to RAG From First Principles. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For groundedness, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Citations

A useful architecture diagram for RAG From First Principles separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For citations, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Rag

Versioning is part of the technical design of RAG From First Principles, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If RAG changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Chunking

The final production question for RAG From First Principles is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For chunking, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Assessment and mastery

### Question 1

Explain how you would design, implement, test, observe and defend **RAG** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 2

Explain how you would design, implement, test, observe and defend **chunking** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 3

Explain how you would design, implement, test, observe and defend **embeddings** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 4

Explain how you would design, implement, test, observe and defend **similarity search** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 5

Explain how you would design, implement, test, observe and defend **groundedness** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 6

Explain how you would design, implement, test, observe and defend **citations** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 7

Explain how you would design, implement, test, observe and defend **RAG** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 8

Explain how you would design, implement, test, observe and defend **chunking** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 9

Explain how you would design, implement, test, observe and defend **embeddings** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 10

Explain how you would design, implement, test, observe and defend **similarity search** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 11

Explain how you would design, implement, test, observe and defend **groundedness** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 12

Explain how you would design, implement, test, observe and defend **citations** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 13

Explain how you would design, implement, test, observe and defend **RAG** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 14

Explain how you would design, implement, test, observe and defend **chunking** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 15

Explain how you would design, implement, test, observe and defend **embeddings** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 16

Explain how you would design, implement, test, observe and defend **similarity search** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 17

Explain how you would design, implement, test, observe and defend **groundedness** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 18

Explain how you would design, implement, test, observe and defend **citations** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 19

Explain how you would design, implement, test, observe and defend **RAG** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 20

Explain how you would design, implement, test, observe and defend **chunking** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 21

Explain how you would design, implement, test, observe and defend **embeddings** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 22

Explain how you would design, implement, test, observe and defend **similarity search** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 23

Explain how you would design, implement, test, observe and defend **groundedness** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 24

Explain how you would design, implement, test, observe and defend **citations** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 25

Explain how you would design, implement, test, observe and defend **RAG** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 26

Explain how you would design, implement, test, observe and defend **chunking** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 27

Explain how you would design, implement, test, observe and defend **embeddings** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 28

Explain how you would design, implement, test, observe and defend **similarity search** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 29

Explain how you would design, implement, test, observe and defend **groundedness** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 30

Explain how you would design, implement, test, observe and defend **citations** in a real RAG From First Principles system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

## Mastery gate

Completion means being able to explain the mechanism from first principles, implement the smallest working version, deliberately break it, identify the first failing boundary from evidence, repair it, measure the repaired system against a baseline, and defend the resulting trade-offs. The learner should also explain when not to use the mechanism. Production expertise includes recognizing when a simpler deterministic solution is safer, cheaper and easier to operate.

## Deep case study 1: Rag

Consider an enterprise workload in which RAG is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why RAG cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 2: Chunking

Consider an enterprise workload in which chunking is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why chunking cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 3: Embeddings

Consider an enterprise workload in which embeddings is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why embeddings cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 4: Similarity Search

Consider an enterprise workload in which similarity search is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why similarity search cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 5: Groundedness

Consider an enterprise workload in which groundedness is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why groundedness cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 6: Citations

Consider an enterprise workload in which citations is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why citations cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 7: Rag

Consider an enterprise workload in which RAG is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why RAG cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 8: Chunking

Consider an enterprise workload in which chunking is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why chunking cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 9: Embeddings

Consider an enterprise workload in which embeddings is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why embeddings cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 10: Similarity Search

Consider an enterprise workload in which similarity search is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why similarity search cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 11: Groundedness

Consider an enterprise workload in which groundedness is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why groundedness cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 12: Citations

Consider an enterprise workload in which citations is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why citations cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 13: Rag

Consider an enterprise workload in which RAG is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why RAG cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 14: Chunking

Consider an enterprise workload in which chunking is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why chunking cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 15: Embeddings

Consider an enterprise workload in which embeddings is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why embeddings cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 16: Similarity Search

Consider an enterprise workload in which similarity search is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why similarity search cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 17: Groundedness

Consider an enterprise workload in which groundedness is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why groundedness cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 18: Citations

Consider an enterprise workload in which citations is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why citations cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 19: Rag

Consider an enterprise workload in which RAG is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why RAG cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 20: Chunking

Consider an enterprise workload in which chunking is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why chunking cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 21: Embeddings

Consider an enterprise workload in which embeddings is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why embeddings cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 22: Similarity Search

Consider an enterprise workload in which similarity search is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why similarity search cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 23: Groundedness

Consider an enterprise workload in which groundedness is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why groundedness cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 24: Citations

Consider an enterprise workload in which citations is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why citations cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 25: Rag

Consider an enterprise workload in which RAG is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why RAG cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 26: Chunking

Consider an enterprise workload in which chunking is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why chunking cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 27: Embeddings

Consider an enterprise workload in which embeddings is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why embeddings cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 28: Similarity Search

Consider an enterprise workload in which similarity search is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why similarity search cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 29: Groundedness

Consider an enterprise workload in which groundedness is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why groundedness cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 30: Citations

Consider an enterprise workload in which citations is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why citations cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 31: Rag

Consider an enterprise workload in which RAG is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why RAG cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 32: Chunking

Consider an enterprise workload in which chunking is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why chunking cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.
