# Practical Agentic AI and RAG Course

> **Industry-oriented companion course and hands-on engineering lab** built around the IITM Pravartak Agentic AI & RAG curriculum, extended into frontier agent engineering.

This repository is the practical engineering workspace for a 38-module learning journey. The first 30 modules preserve the core IITM-aligned progression; Modules 31–38 extend it into loop engineering, harness engineering, long-running agents, skills and memory, environments and verifiers, controlled self-improvement, computer use, always-on workers, and the integrated AegisAI capstone.

## Course philosophy

Many AI courses teach APIs and frameworks first. Real engineering work starts earlier:

- What problem are we solving?
- Does the problem actually need an LLM, RAG, an agent, or a multi-agent system?
- What information must be grounded?
- What can the model be trusted to decide?
- What actions may the system take?
- Who owns the agent's authority?
- How does the system stop, recover and resume?
- How do we verify that the task really succeeded?
- How do we measure quality before and after a change?
- How do we debug a probabilistic system from production evidence?
- How do we control latency, reliability, security, privacy, and cost?

This course trains those decisions first and the frameworks second.

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

The central principle is:

> **LLMs are probabilistic; production software is contractual.**
>
> The engineering discipline comes from the control layer between those worlds: schemas, validation, retrieval, policies, tests, retries, budgets, observability, evaluation, security, and operational limits.

## Learning contract

Learners are expected to:

1. Understand the concept.
2. Implement a working baseline.
3. Break the system intentionally.
4. Diagnose the failure from evidence.
5. Measure quality, latency, reliability, safety, and cost.
6. Improve the design.
7. Document trade-offs.
8. Defend the implementation in an interview-style discussion.

Completion is evidence-based: GitHub artifacts, tests, experiment results, architecture decisions, and mastery assessments matter more than passive lesson completion.

## Continuous capstone: AegisAI

Across the modules we evolve a single platform, **AegisAI**, from a simple AI system into a governed enterprise Agentic RAG and autonomous-work platform.

```text
User / Event
     |
     v
Gateway -> Auth / Tenant -> Task Contract -> Router
                                      |
                  +-------------------+------------------+
                  |                   |                  |
                Simple               RAG                Agent
                                      |                  |
                          Retrieval / Reranker        Harness
                                      |                  |
                                      +--------+---------+
                                               |
                  +----------------------------+-------------------------+
                  |             |              |             |           |
                Tools        Memory         Skills        Computer     MCP
                  |             |              |            Use          |
                  +-------------+--------------+-------------+------------+
                                               |
                                         Policy Engine
                                               |
                                       Agent Loop Engine
                                               |
                                      Verification / Eval
                                               |
                           +-------------------+------------------+
                           |                                      |
                       Approval                               Recovery
                           |                                      |
                           +-------------------+------------------+
                                               |
                                            Result
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
24. **Enterprise MCP Server** — MCP Server

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

Every autonomous capability must answer all twelve questions.

## Module anatomy

Every module follows the same engineering loop:

```text
Problem
  -> Concepts
  -> Internals
  -> Visual architecture
  -> Real-world case
  -> Build
  -> Test
  -> Break
  -> Debug
  -> Measure
  -> Optimize
  -> Secure
  -> Document
  -> Interview
  -> Mastery gate
```

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

The course deliberately injects failures including:

- bad retrieval
- stale and duplicate knowledge
- hallucination
- malformed tool calls
- infinite loops
- no-progress loops
- tool timeouts
- worker crashes
- stale checkpoints
- approval expiry
- unauthorized actions
- prompt injection
- credential leakage
- UI drift
- distributed coordination failures
- cost explosions
- evaluator gaming
- self-improvement regressions

Every failure should become an observable incident with a root cause, containment strategy, recovery path and regression test.

## Interview readiness

Every module includes:

- concept questions
- coding challenges
- debugging challenges
- production incidents
- architecture/system-design prompts
- trade-off questions
- communication/behavioral prompts

The course does **not** guarantee that a learner will pass every interview. It is designed to make interview preparation concrete through working systems, measurements, failure analysis, and defensible engineering decisions.

## GitHub learning evidence

A completed learner should be able to point to:

- runnable code
- tests
- diagrams
- benchmark results
- failure investigations
- architecture decision records (ADRs)
- threat/security notes
- evaluation datasets
- deployment manifests
- a continuously evolving capstone

## QA and deep-practice implementation

The repository now includes a formal 38-module QA standard and a module-specific deep-practice implementation pack. These are used to prevent the common failure mode of having a notebook that exists but is too shallow to teach engineering judgment.

- `00-course-roadmap/COURSE-QA-AUDIT-AND-UPGRADE-PLAN.md` — definition of done and audit matrix
- `00-course-roadmap/COLAB-PRACTICE-NOTEBOOK-STANDARD.md` — required Colab learning sequence
- `00-course-roadmap/MODULE-DEEP-PRACTICE-IMPLEMENTATION-PACK.md` — module-by-module BUILD/TRY/BREAK/MEASURE/DEFEND targets
- `00-course-roadmap/course_qa_checker.py` — executable structural QA checker
- `.github/workflows/course-qa.yml` — CI check for repository learning signals

The QA checker is deliberately non-blocking during the upgrade phase. Once all modules satisfy the contract, CI can be switched to `--strict`. Structural QA is explicitly different from notebook execution QA.

## Source and extension policy

The IITM Pravartak curriculum is treated as the source curriculum for the core module sequencing and terminology. Practical implementation, engineering exercises, benchmarks, security labs, frontier-agent material, and interview preparation are course extensions and should be read as such.

## Current build status

- Core course architecture: established
- Frontier roadmap: established
- Modules 1–38: canonical module structure and Colab notebooks present
- Deep-practice upgrade specification: implemented across all 38 modules
- Structural QA automation: implemented
- Module 6 duplicate directories: retained pending deliberate merge of their useful material
- Notebook execution validation: still requires a dedicated runtime/CI pass and is **not** claimed as complete

The next implementation priority is to close module-specific QA gaps, execute notebook/test validation, and only then enable strict CI completion gates.
