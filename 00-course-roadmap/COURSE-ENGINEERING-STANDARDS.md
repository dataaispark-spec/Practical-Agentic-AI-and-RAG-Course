# Course Engineering Standards — Authoritative Best Practices

**Scope:** Modules 01–43 and their supporting artifacts  
**Status:** **Normative**  
**Canonical branch:** `main`  
**Last updated:** 2026-09-09

This is the primary content and engineering standard for the course. Module-specific documents may add requirements, but they must not contradict this standard. Historical audit reports are evidence, not policy.

## 1. Teaching objective

The course should develop engineers who can:

> **understand → implement → break → debug → measure → secure → optimize → operate → defend** AI systems.

The objective is not to maximize framework familiarity, notebook size, code volume or the number of buzzwords covered.

## 2. Design rules

### 2.1 Mechanism before framework

Teach the underlying state, control flow, data flow, contracts and failure semantics before introducing a framework abstraction. A learner should be able to explain what the framework is doing conceptually.

### 2.2 Minimum sufficient architecture

Choose an architecture from explicit requirements and constraints. A workflow, RAG pipeline, single agent or multi-agent system should be justified by measurable need. “Agentic” is not a requirement.

### 2.3 Deterministic control around probabilistic behavior

Treat model output as a proposal, not an authority. Deterministic code should enforce:

- schemas and validation;
- identity and tenant binding;
- authorization and capability limits;
- policy precedence;
- budgets and deadlines;
- state transitions;
- approval requirements;
- termination conditions;
- idempotency/replay protection;
- audit records.

### 2.4 Explicit state

For every stateful system, identify:

- owner;
- type/schema;
- lifetime;
- persistence location;
- source of truth;
- consistency/recovery semantics;
- revocation or invalidation behavior.

Distinguish ephemeral context, durable state, authoritative records and advisory memory.

### 2.5 Contracts at boundaries

Use typed, versioned contracts for APIs, tools, agent messages, retrieval records, graph claims, checkpoints and evaluation events. Validate both inputs and outputs.

### 2.6 Failure-first development

For every important mechanism, define at least one invariant and intentionally violate it. Show the symptom, diagnose the first failure, repair it and add a regression assertion.

### 2.7 Verification independent of self-report

A model saying “done” is not proof. When feasible, use an independent verifier based on postconditions, deterministic checks, external evidence or a separate evaluator. State clearly when verification is probabilistic or incomplete.

### 2.8 Bounded autonomy

Use explicit limits for steps, context/tokens, tool calls, time, money, concurrency, retries and recursion. Include cancellation and safe-stop behavior.

### 2.9 Persistence-aware security

Anything durable can become a poisoning or integrity surface: memory, skills, graph updates, prompts, tools, policies and artifacts. Require provenance, validation, promotion gates, versioning and rollback for trusted persistence.

### 2.10 Reproducible releases

The release identity of an AI system should capture more than application code. Where applicable include model/provider, prompt/template, retrieval/index/embedding version, tool/MCP contract, policy configuration, evaluation set/version and deployable artifact.

## 3. Practical artifact standard

Each canonical module should expose, directly or through explicit links:

```text
Objectives
→ Theory / mechanism
→ Concept map
→ Architecture + data/control flow
→ Minimal runnable implementation
→ Guided practice
→ Failure-first exercise
→ Measurement
→ Security / misuse
→ Independent challenge
→ System design
→ Reference solution
→ Tests / assertions
→ Interview practice
→ Mastery gate
→ AegisAI / next-module bridge
```

Do not force every topic into identical prose or file counts. The evidence should fit the module.

## 4. Worked-example standard

A good explanation moves from small to realistic:

1. smallest mechanism;
2. instrumented example;
3. realistic synthetic scenario;
4. intentionally broken variant;
5. production constraints;
6. design decision and trade-offs.

Do not introduce five technologies when one local implementation can expose the mechanism clearly.

## 5. Industry realism

Use synthetic but credible scenarios across banking/payments, healthcare, cybersecurity/SOC, manufacturing, enterprise IT/SRE, e-commerce/procurement, legal/policy, software engineering and sales/research.

A scenario is useful when it changes the engineering problem through constraints such as SLA, tenant isolation, approval, evidence, cost, partial failure or data freshness.

## 6. Security-by-construction baseline

Relevant modules should explicitly model:

```text
Identity
  ↓
Authentication
  ↓
Authorization / least privilege
  ↓
Policy
  ↓
Budget / approval
  ↓
Action
  ↓
Verification
  ↓
Audit
```

Untrusted content includes retrieved documents, webpages, memory records, graph claims, tool output, MCP responses, screenshots and model-generated strings unless explicitly promoted through a trust boundary.

For consequential action, require exact action binding where practical and prevent replay/duplicate effects.

## 7. RAG and knowledge quality

RAG teaching must separate:

- source truth;
- transformation/parsing;
- retrieval;
- evidence selection;
- generation;
- citation/provenance;
- authorization.

Measure retrieval before claiming generation quality. Where applicable compare vector-only, lexical/hybrid, graph and reranked variants. Include cases where a more complex retriever is worse.

Graph systems additionally require bounded traversal, provenance, temporal validity when needed, entity resolution, contradiction/supersession handling and graph-poisoning tests. Graph evidence must not directly become action authority.

## 8. Agent and multi-agent quality

Agent systems should expose the loop explicitly:

```text
OBSERVE → DECIDE → ACT → VERIFY → RECOVER / STOP → RECORD
```

Multi-agent systems must begin with a single-agent baseline when practical and quantify whether delegation adds enough value to justify coordination, security and latency overhead.

Delegation should use typed task envelopes, capability restrictions, deadlines, failure classification and idempotency.

## 9. Evaluation standard

Evaluation should be multidimensional. Select metrics relevant to the module and interpret them:

- task success/correctness;
- retrieval quality;
- groundedness/citation correctness;
- safety/policy violations;
- reliability/recovery;
- latency/throughput;
- token/tool/compute cost;
- operational diagnostics.

Use regression sets, meaningful slices and confidence/uncertainty where appropriate. Do not overclaim from small or cherry-picked datasets.

## 10. Notebook standard

The canonical notebook requirements live in [`COLAB-PRACTICE-NOTEBOOK-STANDARD.md`](./COLAB-PRACTICE-NOTEBOOK-STANDARD.md). At minimum, every substantive notebook must provide executable evidence for:

`Predict → Build → Try → Observe → Break → Debug → Measure → Improve → Defend`

Core learning must be runnable without paid API keys.

## 11. Testing standard

Tests should cover both success and failure invariants. Prefer deterministic, local fixtures for the educational baseline.

When tests are modified:

- avoid brittle exact floating-point equality;
- verify meaningful behavior rather than implementation trivia;
- cover security boundaries and duplicate side effects where applicable;
- preserve a regression test for every important fixed defect;
- keep optional vendor integrations separate from the core CI path.

## 12. Change and versioning policy

Changes to model/provider, prompts, retrieval, tools, policies, schemas or evaluation can alter behavior even when application code is unchanged. Teach and test version identity accordingly.

Fast-changing product claims must be dated/source-backed in module material. Do not teach a current vendor feature as a timeless principle.

## 13. Anti-patterns to remove

Remove or rewrite content that primarily consists of:

- repetitive definitions;
- generic “AI is transforming…” introductions;
- framework feature lists without mechanisms;
- code that cannot be inspected or modified meaningfully;
- notebook cells that only print predetermined prose;
- fake metrics with no experimental question;
- security sections that name threats but do not demonstrate a boundary;
- solution dumps before learner challenges;
- excessive vendor branding in place of engineering concepts;
- duplicated standards copied across many modules;
- claims that CI/file presence proves pedagogical quality;
- word-count padding.

## 14. Mastery evidence

A learner should progressively demonstrate:

| Level | Evidence |
|---|---|
| L1 | Explain mechanism, assumptions and limits. |
| L2 | Implement a minimal correct version. |
| L3 | Break and debug it. |
| L4 | Measure and optimize it. |
| L5 | Design under production constraints. |
| L6 | Defend trade-offs using evidence. |
| L7 | Transfer the skill to a novel scenario. |

The final gate should be difficult to pass by copying a previous cell verbatim.

## 15. AegisAI progression

AegisAI is the shared long-running capstone context. A module should add a distinct primitive or constraint rather than rebuilding an unrelated toy.

The progression is:

```text
Architecture
→ AI application engineering
→ RAG
→ tools / loops / memory / state / planning / security
→ multi-agent / MCP
→ production engineering
→ knowledge + graph engineering
→ loop / harness engineering
→ durable autonomy
→ continual skills / memory
→ environments / verifiers / agentic RL
→ recursive improvement
→ computer use
→ frontier capstone
```

## 16. Certification standard

Certification is layered:

```text
Structure
→ Unit/module tests
→ Clean-kernel notebook runtime
→ Aggregate CI
→ Manual semantic review
→ Certification
```

A course is not certified solely because the repository has the expected folders, and a notebook is not practice-complete solely because it executes.
