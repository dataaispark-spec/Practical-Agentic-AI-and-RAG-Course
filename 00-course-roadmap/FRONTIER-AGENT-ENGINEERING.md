# Frontier Agent Engineering Track

**Scope:** Modules 36–43  
**Status:** normative subject-matter guidance  
**Canonical branch:** `main`  
**Updated:** 2026-09-09

This track extends the production Agentic RAG foundation into frontier agent engineering. It is **not** a collection of product tutorials. It teaches reusable mechanisms: loop engineering, harnesses, durable state, skills, environments, verifiers, continual improvement, computer use and agentic reinforcement learning.

For course-wide rules, see [`COURSE-ENGINEERING-STANDARDS.md`](./COURSE-ENGINEERING-STANDARDS.md).

## Frontier mental model

> **Production agent = model + harness + environment + tools + state + policy + verification + evaluation.**

```text
                    MODEL
                      |
                      v
             +----------------+
             |     HARNESS    |
             | loop / state   |
             | tools / skills |
             | policy / budget|
             +-------+--------+
                     |
                     v
                ENVIRONMENT
                /          \
          OBSERVATION     ACTION
                \          /
                 v        v
                   VERIFIER
                       |
                       v
                   EVALUATOR
                   /       \
              DEPLOY     IMPROVE
                   \       /
                    v     v
                  NEXT TRAJECTORY
```

The model may propose. The harness and environment enforce what can actually happen.

## Module progression

| Module | Focus | New systems constraint |
|---:|---|---|
| 36 | Loop Engineering | explicit loop ownership, halting, recovery and trajectory control |
| 37 | Harness Engineering | reusable control plane around models, tools, state and policy |
| 38 | Long-Running Autonomous Agents | durable execution, leases, checkpoints, waiting and resume |
| 39 | Skills, Memory & Continual Harnesses | trusted skill promotion, persistent memory and behavioral evolution |
| 40 | Environments, Verifiers & Agentic RL | explicit tasks, environment contracts, deterministic verification and reward design |
| 41 | Recursive Self-Improving Agents | controlled improvement proposals, experiments, gates and rollback |
| 42 | Computer Use & Always-On AI Teammates | grounded UI actions, stale state, approval and persistent scheduling |
| 43 | Frontier Graph-RAG Agentic Capstone | integrated governed autonomous enterprise system |

## Cross-cutting control questions

Every frontier module should answer:

| Dimension | Engineering question |
|---|---|
| Goal | What counts as successful completion? |
| Loop | Who owns the next transition? |
| State | What survives restart, and what is authoritative? |
| Tools | What capabilities are exposed? |
| Policy | What can never be done or requires approval? |
| Budget | What limits apply to time, context, steps, tools and money? |
| Verification | What independently proves correctness? |
| Recovery | What happens after partial failure? |
| Evaluation | How are versions compared? |
| Improvement | What evidence permits promotion? |
| Security | Which trust boundary could be crossed? |
| Audit | Can the trajectory and side effects be reconstructed? |

## Frontier principles

### Mechanism before product

Case studies from current agent products/research are useful only when learners extract the underlying primitive and implement a minimal version independently.

### Deterministic controls remain outside the model

Schemas, authorization, budgets, deadlines, state transitions, approvals, termination and audit should be enforceable without trusting the model to follow a textual instruction.

### Verification is a first-class subsystem

Autonomy without a meaningful success signal is not robust autonomy. Verification should be task-specific and independent when practical.

### Persistence changes the threat model

A long-lived worker can accumulate memory, permissions, credentials, artifacts, schedules and behavioral drift. Lifecycle controls must therefore cover revocation, expiry, provenance, rollback and recovery.

### Self-improvement requires promotion gates

Changing prompts, skills, tools, memory, models or policies is a change to system behavior. The candidate must be evaluated against a baseline and held-out/regression cases before promotion. Always retain a rollback path.

### Reward is not truth

Agentic RL introduces the risk of reward hacking, evaluator gaming, specification gaming and distribution shift. Reward design, verifier design and held-out evaluation must be taught separately.

## Frontier security labs

Relevant failure injections include:

- infinite loops and oscillation;
- retry storms and budget bypass;
- stale checkpoints and duplicated effects;
- malicious skill/memory/graph updates;
- capability escalation through delegation;
- forged/stale approvals;
- prompt/document/tool poisoning;
- stale computer-use screenshots/DOM state;
- unintended credential exposure or egress;
- verifier blind spots and reward hacking;
- self-improvement evaluator gaming.

A useful failure record is:

```text
setup
→ injected fault
→ expected symptom
→ violated invariant
→ diagnosis
→ recovery
→ regression test
```

## Research/product fact policy

Because frontier systems change quickly, module material must distinguish:

1. stable engineering principles;
2. current product/framework behavior;
3. experimental research claims;
4. vendor/lab benchmark claims;
5. learner-generated measurements.

Current product features and benchmark numbers must be checked against authoritative current sources before being presented as current facts. Benchmark results must include their evaluation setup and limitations.

## Mastery standard

A learner completing the frontier track should be able to:

1. build a framework-free bounded agent loop;
2. wrap it in a governed harness;
3. persist and recover state safely;
4. introduce skills and memory with trust gates;
5. delegate work under capability and budget constraints;
6. execute asynchronously for long periods with leases/checkpoints;
7. verify outcomes independently;
8. construct environment tasks and deterministic verifiers;
9. inspect trajectories and diagnose reward/verification failures;
10. run controlled self-improvement with evaluation and rollback;
11. ground computer-use actions against current environment state;
12. design the integrated frontier AegisAI system under security, reliability, cost and audit constraints.
