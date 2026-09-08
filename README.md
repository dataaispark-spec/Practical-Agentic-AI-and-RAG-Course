# Practical Agentic AI and RAG Course

> **Industry-oriented companion course and hands-on engineering lab** built around the IITM Pravartak Agentic AI & RAG curriculum, extended into frontier agent engineering.

This repository is the practical engineering workspace for a **38-module** learning journey. Modules 1–30 preserve the core IITM-aligned progression; Modules 31–38 extend it into loop engineering, harness engineering, long-running agents, skills and memory, environments and verifiers, controlled self-improvement, computer use, always-on workers, and the integrated AegisAI frontier capstone.

## Course philosophy

This is not an API-tour course. It is an engineering course built around a repeated question: **what must be deterministic around a probabilistic model to make the system reliable?**

Learners repeatedly answer:

- What problem are we solving?
- Does it need an LLM, RAG, an agent, or multiple agents?
- What information must be grounded?
- What may the model decide?
- What actions may the system take?
- Who owns authority and approval?
- How does the system stop, recover, restart, and resume?
- How do we verify that the task actually succeeded?
- How do we measure quality, latency, reliability, safety, and cost?
- How do we debug from production evidence?
- How do we improve a system without silently degrading it?

**Frameworks come after mechanisms.** The course uses small, inspectable implementations before introducing framework-level abstractions.

## Core mental model

```text
Agent
 = Model
 + Harness
 + Environment
 + Tools
 + State
 + Policy
 + Verification
 + Evaluation
```

The central engineering principle is:

> **LLMs are probabilistic; production software is contractual.**
>
> Reliability comes from the control layer between those worlds: contracts, schemas, validation, retrieval, policy, tests, retries, budgets, observability, evaluation, security, persistence, and operational limits.

## Learning contract

For every module, the learner should:

1. Understand the problem and mechanism.
2. Implement a working baseline.
3. Run the supplied tests/examples.
4. Break the system intentionally.
5. Diagnose the failure from evidence.
6. Measure meaningful quality/operations/security signals.
7. Improve the implementation.
8. Document trade-offs and production implications.
9. Defend the design in interview/system-design discussion.

Completion is **evidence-based**: runnable artifacts, tests, experiments, failure investigations, architecture decisions, and mastery gates matter more than passive lesson completion.

## Continuous capstone — AegisAI

Across the course we evolve one platform, **AegisAI**, from a simple AI application into a governed enterprise Agentic RAG and autonomous-work platform.

```text
User / Event
     |
Gateway -> Auth / Tenant -> Task Contract -> Router
                                      |
             +------------------------+----------------------+
             |                        |                      |
           Simple                    RAG                   Agent
                                      |                      |
                              Retrieval / Reranker        Harness
                                      |                      |
             +------------------------+----------------------+
             |          |          |          |              |
           Tools      Memory     Skills     MCP        Computer Use
             |          |          |          |              |
             +----------+----------+----------+--------------+
                                      |
                               Policy / Budget
                                      |
                                 Agent Loop
                                      |
                           Verification / Evaluation
                                      |
                       Approval / Recovery / Durability
                                      |
                          Audit / Observability / Metrics
                                      |
                           Controlled Improvement
```

## 38-module progression

### Foundation

1. **AI Systems Thinking & Architecture Decisions** — AI Architecture Decision Engine
2. **Python for AI Engineering** — Production Async LLM Client
3. **FastAPI + Testing** — Streaming AI API
4. **LLM Application Foundations** — Multi-Model Router
5. **Prompting + Evaluation** — LLM Evaluation Harness

### RAG Engineering

6. **RAG From First Principles** — NumPy RAG Engine
7. **Embeddings + Vector Databases** — Vector Search Benchmark
8. **Document Intelligence + PII** — Enterprise Document Pipeline
9. **Advanced Retrieval** — Hybrid + Reranked RAG
10. **RAG Optimization** — Cached / Versioned Knowledge Platform
11. **RAG Evaluation** — Automated RAG Evaluation Framework
12. **RAG Debugging** — RAG Failure Investigation Lab

### Agent Engineering

13. **Tool Calling + API Agents** — Data Agent
14. **Raw Agent Loop** — Agent from Scratch
15. **Memory** — Multi-Tier Agent Memory
16. **LangGraph** — Stateful Agent Workflow
17. **Planning + Human-in-the-Loop** — Planner/Executor Agent
18. **Agent Security** — Secure Grounded Agent

### Multi-Agent Systems

19. **Single vs Multi-Agent Decision Science** — Decision Engine
20. **Multi-Agent Architectures** — Supervisor/Worker System
21. **Coordination + Fault Tolerance** — Fault-Tolerant Agent Network
22. **Multi-Agent Debugging** — Distributed Agent Debugging Lab

### MCP

23. **MCP Fundamentals** — MCP Client
24. **Enterprise MCP Server** — Governed MCP Server

### Production AI

25. **Observability** — AI Observability Platform
26. **Production Evaluation + Regression** — Evaluation System
27. **Cost Engineering** — Cost-Aware AI Router
28. **Responsible AI + Security** — AI Governance Layer
29. **Deployment + CI/CD** — Production Deployment Pipeline
30. **Enterprise Agentic RAG Capstone** — Complete AegisAI Platform

### Frontier Agent Engineering

31. **Loop Engineering** — Production Agent Loop Engine
32. **Harness Engineering** — AegisAI Agent Harness
33. **Long-Running & Autonomous Agents** — Durable Autonomous Worker
34. **Skills, Memory & Continual Harnesses** — Self-Improving AegisAI
35. **Environments, Verifiers & Agentic RL** — Agent Training Environment
36. **Recursive / Self-Improving Agents** — Research Agent Harness
37. **Computer Use & Always-On AI Teammates** — Enterprise Digital Worker
38. **Frontier Agentic RAG Capstone** — AegisAI Autonomous Enterprise Platform

## Frontier control plane

The frontier modules share a common control-plane model:

```text
Goal
 ↓
Loop
 ↓
State
 ↓
Tools
 ↓
Policy
 ↓
Budget
 ↓
Verification
 ↓
Recovery
 ↓
Evaluation
 ↓
Improvement
 ↓
Security
 ↓
Audit
```

Every autonomous capability must be able to answer all twelve questions.

## Module anatomy

Every module follows the same engineering loop:

```text
Problem
  -> Concepts
  -> Internals
  -> Architecture / Diagram
  -> Industry Scenario
  -> Guided Build
  -> Tests
  -> Failure Injection
  -> Debugging
  -> Measurement
  -> Optimization
  -> Security
  -> Documentation
  -> Interview / System Design
  -> Mastery Gate
```

The Colab practice standard expands this into a **Predict → Run → Observe → Explain → Break → Debug → Measure → Improve → Defend** cycle. Notebooks are intended to be executable learning environments, not merely slide decks.

## Engineering ladder

```text
L1 Explain
L2 Implement
L3 Debug
L4 Optimize
L5 Design
L6 Defend trade-offs
L7 Solve unfamiliar problems
```

The objective is to move repeatedly through all seven levels.

## Failure-first engineering

The course deliberately injects failures such as:

- retrieval misses, stale knowledge, duplicate knowledge, and hallucination
- malformed tool calls and poisoned tool output
- infinite/no-progress loops and retry storms
- worker crashes, stale checkpoints, duplicate side effects, and approval expiry
- prompt injection, memory poisoning, credential leakage, SSRF-style abuse, and cross-tenant access
- distributed coordination races, delayed/lost messages, overload, and partial failure
- UI drift, stale screens, duplicate submissions, and unattended destructive actions
- cost explosions and budget bypass
- evaluator gaming, reward hacking, benchmark leakage, and self-improvement regressions

A meaningful failure is expected to become an observable incident with a root cause, containment strategy, recovery path, and regression test.

## Frontier engineering principles

1. **Framework second, mechanism first.**
2. **Deterministic control around probabilistic decisions.**
3. **Verification is first-class.**
4. **Persistence changes the threat model.**
5. **Self-improvement requires external gates.**
6. **Long-running autonomy requires durable state, leases, budgets, and recovery.**
7. **Computer use requires environment grounding, policy checks, approval boundaries, and post-action verification.**
8. **More agents are not automatically better; multi-agent complexity must earn its cost and risk.**

## Interview readiness

Every module includes some combination of:

- concept questions
- coding challenges
- debugging challenges
- production incidents
- architecture/system-design prompts
- trade-off questions
- security/privacy scenarios
- communication/behavioral prompts

The course does **not** guarantee that a learner will pass every interview. It is designed to make preparation concrete through working systems, measurements, failure analysis, and defensible engineering decisions.

## GitHub learning evidence

A strong completion portfolio should contain:

- runnable implementations
- tests and assertions
- architecture diagrams and ADRs
- Colab experiments and observations
- benchmark/evaluation results
- failure investigations and regression tests
- threat/security notes
- deployment/release artifacts
- a continuously evolving AegisAI capstone

## QA, checkpoints, and deep-practice standard

The repository includes explicit QA documentation so that **"a notebook exists" is not mistaken for "the module is deeply teachable and executable."**

- `00-course-roadmap/COURSE-QA-AUDIT-AND-UPGRADE-PLAN.md` — 38-module definition of done and audit matrix
- `00-course-roadmap/COLAB-PRACTICE-NOTEBOOK-STANDARD.md` — required deep-practice notebook sequence
- `00-course-roadmap/MODULE-DEEP-PRACTICE-IMPLEMENTATION-PACK.md` — module-by-module BUILD / TRY / BREAK / MEASURE / DEFEND targets
- `00-course-roadmap/course_qa_checker.py` — executable structural QA checker
- `00-course-roadmap/run_notebook_qa.py` — clean-kernel notebook execution runner
- `.github/workflows/course-qa.yml` — structural, module-test, notebook-runtime, and final aggregate CI gates

**Important:** structural QA, module tests, and notebook execution are separate evidence layers. A green structural check does not prove runtime correctness; a passing notebook does not prove pedagogical completeness.

## Current checkpoint — 2026-09-08

- 38-module course architecture: **established**
- Frontier roadmap and control plane: **established**
- Modules 1–38 canonical structure/notebooks: **present**
- Deep-practice QA specification: **established**
- Runtime QA runner/dependency baseline: **implemented**
- Frontier runtime implementations for Modules 31–37: **implemented with tests**
- Module 06 duplicate: **consolidated to `06-rag-from-first-principles/` and old duplicate artifacts removed**
- Latest M06–M09 hardening: **implemented** for deterministic ranking/filtering, embedding reproducibility, PII/provenance controls, and authorization-before-candidate-truncation
- CI module identifiers: **hardened to preserve zero-padded module paths**
- Latest CI: **re-triggered; final green status not yet claimed until the full matrix completes**

### Definition of done

The course should only be called **38-module QA complete** when all of the following are evidenced on the same current revision:

1. structural QA passes;
2. all 35 module-test jobs for Modules 04–38 pass;
3. all 35 notebook-runtime jobs for Modules 04–38 pass;
4. the final aggregate QA gate passes;
5. Modules 31–38 retain real runnable implementations, not notebook-only placeholders;
6. every module meets the deep-practice notebook contract or has an explicitly documented exception;
7. no duplicate/ambiguous canonical module paths remain.

Until then, the repository status is **upgrade + validation in progress**, not "fully QA certified."

## Source and extension policy

The IITM Pravartak curriculum is treated as the source curriculum for the core module sequencing and terminology. Practical implementation, engineering exercises, benchmarks, security labs, frontier-agent material, and interview preparation are course extensions and should be read as such. Where an implementation is intentionally educational/deterministic rather than production infrastructure, the module documentation should say so explicitly.
