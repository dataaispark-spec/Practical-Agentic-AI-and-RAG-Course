# Practical Agentic AI and RAG Course

> **Industry-oriented companion course and hands-on engineering lab** built around the IITM Pravartak Agentic AI & RAG curriculum.

This repository is the practical engineering workspace for a 30-module Agentic AI and RAG learning journey. The source curriculum provides the academic/module structure; this repository extends that structure with production-style implementation, experiments, debugging, evaluation, security, system design, and interview preparation.

## Why this course exists

Many AI courses teach APIs and frameworks first. Real engineering work starts earlier:

- What problem are we solving?
- Does the problem actually need an LLM, RAG, an agent, or a multi-agent system?
- What information must be grounded?
- What can the model be trusted to decide?
- What actions may the system take?
- How do we measure quality before and after a change?
- How do we debug a probabilistic system from production evidence?
- How do we control latency, reliability, security, privacy, and cost?

This course trains those decisions first and the frameworks second.

## Learning contract

Learners are expected to:

1. Understand the concept.
2. Implement a working baseline.
3. Break the system intentionally.
4. Diagnose the failure from evidence.
5. Measure the relevant quality, latency, reliability, safety, and cost dimensions.
6. Improve the design.
7. Document trade-offs.
8. Defend the implementation in an interview-style discussion.

Completion is evidence-based: GitHub artifacts, tests, experiment results, architecture decisions, and mastery assessments matter more than passive lesson completion.

## Visual mental model

```text
                 BUSINESS PROBLEM
                        |
                        v
                 SYSTEM REQUIREMENTS
                        |
              +---------+---------+
              |                   |
              v                   v
          KNOWLEDGE            ACTION
              |                   |
              v                   v
             RAG                AGENT
              |                   |
              +---------+---------+
                        |
                        v
                  LLM / MODEL
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
      Guardrails     Evaluation    Observability
          |             |             |
          +-------------+-------------+
                        |
                        v
                    PRODUCTION
```

## Continuous capstone: AegisAI

Across the modules we evolve a single platform, **AegisAI**, from a simple AI system into an enterprise-grade Agentic RAG platform.

```text
User
  |
  v
API Gateway --> Auth / Tenant Context --> Router
                                    |
                    +---------------+---------------+
                    |               |               |
                  Simple           RAG            Agent
                    |               |               |
                    v               v               v
                   LLM       Retrieval Stack      Planner
                                  |                 |
                           +------+-----+        Tools
                           |            |
                        Vector       Reranker
                           |            |
                           +-----+------+ 
                                 |
                                LLM
                                 |
                  +--------------+--------------+
                  |              |              |
               Memory       Guardrails      Evaluator
                  |              |              |
                  +--------------+--------------+
                                 |
                             Response
```

## 30-module progression

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

## Core engineering principle

> **LLMs are probabilistic; production software is contractual.**
>
> The engineering discipline comes from the control layer between those worlds: schemas, validation, retrieval, policies, tests, retries, observability, evaluation, security, and operational limits.

## Source and extension policy

The IITM Pravartak curriculum is treated as the source curriculum for module sequencing and terminology. Practical implementation, engineering exercises, benchmarks, security labs, and interview material in this repository are course extensions and should be read as such.

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

## Current status

- Introduction: established
- Module 1: reference chapter established
- Modules 2–30: staged expansion using the Module 1 template
