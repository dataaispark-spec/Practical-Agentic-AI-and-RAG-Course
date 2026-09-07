# Frontier Agent Engineering Track

## Purpose

This track extends the IITM-aligned core curriculum into the 2026 frontier of production agent engineering. It is not a collection of product tutorials. It teaches the underlying engineering ideas that recur across agent systems: **loop engineering, harness engineering, durable state, skills, environments, verifiers, computer use, continual improvement, and agentic reinforcement learning**.

The core rule is:

> A capable model is only one component. The production system is the model plus its harness, environment, policies, state, tools, verification and evaluation loops.

## Why this track exists

Current agent systems increasingly behave like persistent workers rather than chat sessions. Hermes Agent exposes persistent memory, skills, Bot Mode, MCP, scheduled tasks, delegation and programmatic tool calling. Grok Bot is designed around persistent AI teammates with their own computers, applications, memory, autonomous work and approval boundaries. Prime Agent introduces a self-improving coding harness built around Recursive Language Models and a Continual Harness. These systems demonstrate a shift from **prompting a model** toward **engineering an operating environment for an agent**.

These are case studies, not dependencies. Learners implement the principles themselves before studying frameworks/products.

## Revised 2026 course architecture

### Core 30-module foundation

1. AI Systems Thinking & Architecture Decisions
2. Python for AI Engineering
3. FastAPI + Testing
4. LLM Application Foundations
5. Prompting + Evaluation
6. RAG From First Principles
7. Embeddings + Vector Databases
8. Document Intelligence + PII
9. Advanced Retrieval
10. RAG Optimization
11. RAG Evaluation
12. RAG Debugging
13. Tool Calling + API Agents
14. Raw Agent Loop
15. Memory
16. Stateful Agent Workflows
17. Planning + Human-in-the-Loop
18. Agent Security
19. Single vs Multi-Agent Decision Science
20. Multi-Agent Architectures
21. Coordination + Fault Tolerance
22. Multi-Agent Debugging
23. MCP Fundamentals
24. Enterprise MCP Server
25. Observability
26. Production Evaluation + Regression
27. Cost Engineering
28. Responsible AI + Security
29. Deployment + CI/CD
30. Enterprise Agentic RAG Capstone

### Frontier extension

31. **Loop Engineering** — Production Agent Loop Engine
32. **Harness Engineering** — AegisAI Agent Harness
33. **Long-Running Autonomous Agents** — Durable Autonomous Worker
34. **Skills, Memory & Continual Harnesses** — Self-Improving AegisAI
35. **Environments, Verifiers & Agentic RL** — Agent Training Environment
36. **Recursive / Self-Improving Agents** — Research Agent Harness
37. **Computer Use & Always-On AI Teammates** — Enterprise Digital Worker
38. **Frontier Agentic RAG Capstone** — AegisAI Autonomous Enterprise Platform

## Cross-cutting engineering spine

Every module after Module 12 should explicitly answer:

| Control dimension | Required question |
|---|---|
| Goal | What constitutes successful completion? |
| Loop | Who controls the next step: code, model, scheduler, or human? |
| State | What state exists and what survives a restart? |
| Tools | What can the agent access? |
| Policy | What actions are forbidden or approval-gated? |
| Budget | What are time, token, tool-call and monetary limits? |
| Verification | How do we know the result is correct? |
| Recovery | Can the system resume after partial failure? |
| Evaluation | Can two versions be compared objectively? |
| Improvement | What evidence can change future behavior? |
| Security | Can the agent cross its intended trust boundary? |
| Audit | Can the complete decision/action history be reconstructed? |

## New mental model

```text
                    MODEL
                      |
                      v
             +----------------+
             |   HARNESS      |
             |                |
             | loop / state   |
             | tools / skills |
             | policy / budget|
             +-------+--------+
                     |
                     v
                ENVIRONMENT
                     |
              +------+------+
              |             |
              v             v
           ACTION        OBSERVATION
              |             |
              +------+------+
                     |
                     v
                 VERIFIER
                     |
                     v
                 EVALUATOR
                     |
             +-------+-------+
             |               |
          deploy          improve
             |               |
             +-------+-------+
                     |
                     v
                NEXT TRAJECTORY
```

## Frontier engineering principles

### 1. Framework second, mechanism first

Learners must implement a minimal mechanism before relying on LangGraph, AutoGen, Crew-style abstractions, MCP frameworks or product-specific runtimes. Frameworks are then compared against the handwritten baseline.

### 2. Deterministic control around probabilistic decisions

The model may propose. The runtime should enforce:

- schemas
- authorization
- resource budgets
- deadlines
- tool allowlists
- state transitions
- approval requirements
- termination conditions
- audit records

### 3. Verification is a first-class component

An agent that can act without a meaningful success signal is not an engineered autonomous system; it is an uncontrolled loop.

### 4. Persistence changes the threat model

A persistent agent can accumulate memory, permissions, credentials, artifacts, scheduled work and behavioral drift. Long-running systems therefore require lifecycle controls, not merely conversation history.

### 5. Self-improvement requires gates

Any agent that can modify its prompts, skills, memory, tools, sub-agents or policies must pass evaluation and rollback gates. The ability to change itself is not evidence that the change is beneficial.

## Frontier case-study matrix

| System / idea | Course concept | What learners extract |
|---|---|---|
| Hermes Agent | skills, memory, delegation, Bot Mode, MCP, scheduled work | durable agent architecture and progressive capability loading |
| Grok Bot | persistent computer, always-on work, app access, approval | long-running worker and human delegation model |
| Prime Agent | Recursive Language Model, Continual Harness | self-improving harness and programmatic orchestration |
| Agentic RL systems | environments, rollouts, verifiers, rewards | engineering the improvement loop |

Do not teach these as magic products. Ask: **what primitive is underneath the product?**

## Mastery standard for the frontier track

A learner should be able to:

1. Build an agent loop without a framework.
2. Turn it into a durable harness.
3. Add persistent state safely.
4. Add skills with progressive disclosure.
5. Add sub-agent delegation with budgets.
6. Add MCP with least-privilege tool exposure.
7. Run work asynchronously for hours or days.
8. Resume after process failure.
9. Verify task completion independently of the agent's self-report.
10. Construct an environment and measurable verifier.
11. Generate and inspect trajectories.
12. Explain when prompting, workflow engineering, harness engineering, SFT or RL is the appropriate lever.
13. Detect reward hacking.
14. Roll back a harmful self-improvement.
15. Design a secure always-on enterprise agent.

## Research policy

Because this area changes unusually quickly, the course maintains a research log. Every frontier chapter should distinguish:

- stable engineering principles
- current framework/product behavior
- experimental research claims
- benchmark claims from vendors or labs
- learner-generated measurements

Product features must be rechecked against current official documentation before a lab is run. Benchmark numbers should never be presented as universal truth without their evaluation setup.
