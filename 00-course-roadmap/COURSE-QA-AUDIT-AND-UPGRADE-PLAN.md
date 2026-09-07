# Comprehensive 38-Module Course QA Audit & Upgrade Plan

**Audit target:** `Practical-Agentic-AI-and-RAG-Course`  
**Scope:** Modules 1–38, theory, concepts, diagrams, exercises, labs, industry use cases, implementation, tests, Google Colab practice, challenge/solution coverage, assessment and interview readiness.

## Audit standard

Every module should ultimately provide the following learning loop:

```text
Theory
  ↓
Concept map
  ↓
Architecture / diagrams
  ↓
Worked example
  ↓
Runnable implementation
  ↓
Google Colab practice
  ↓
Guided exercise
  ↓
Independent challenge
  ↓
Failure injection / debugging
  ↓
Measurement / evaluation
  ↓
Industry scenario
  ↓
Production hardening
  ↓
Solution / reference implementation
  ↓
Interview + system design
  ↓
Mastery gate
```

### Quality dimensions

| Dimension | Required evidence |
|---|---|
| Theory | definitions, mental models, mechanisms, assumptions, limitations |
| Concepts | prerequisite links, terminology, trade-offs, common misconceptions |
| Diagrams | architecture, data/control flow, failure/recovery path |
| Worked examples | small example before production complexity |
| Implementation | step-by-step build with typed contracts and tests |
| Labs | guided experiments with observable outputs |
| Exercises | progressive L1–L7 difficulty |
| Failure labs | intentionally broken implementation + diagnosis |
| Industry | banking, healthcare, cybersecurity, manufacturing, enterprise IT, e-commerce/legal as appropriate |
| Colab | executable, dependency-light, synthetic data, practice cells, challenge cells |
| Solutions | hints first, reference solution, expected output, explanation |
| Evaluation | correctness, quality, safety, latency, cost, reliability where applicable |
| Security | trust boundaries, abuse cases, controls |
| Assessment | quiz, coding, debugging, architecture and mastery gate |
| Interview | conceptual, coding, debugging, production and system design |
| Capstone | connection to AegisAI and later modules |

## Current repository findings

The recursive Git tree confirms a canonical notebook for each module 1–38. Module 1 has the richest supporting structure, while many later modules currently concentrate material in `README.md`, `app/`, `tests/`, and `notebooks/`. The repository also contains both `06-rag-first-principles` and `06-rag-from-first-principles`; these should be merged deliberately rather than deleting useful material blindly.

### Important distinction

A module **having a notebook is not equivalent to having a complete practical learning experience**. Several existing notebooks are compact lab packs rather than full teaching notebooks. The upgrade therefore targets depth, not merely file presence.

## Module-by-module QA matrix

### Foundation: Modules 1–5

| # | Module | Required practical emphasis | QA priority |
|---|---|---|---|
| 1 | AI Systems Thinking & Architecture Decisions | architecture ladder, requirements decomposition, build-vs-buy, RAG vs workflow vs agent, KPI/constraint trade-offs, ADR exercise, failure-first design | **High** |
| 2 | Python for AI Engineering | typing, dataclasses, async/await, concurrency, cancellation, retries/backoff, timeouts, streaming, structured errors, testability | **High** |
| 3 | FastAPI + Testing | API contracts, validation, streaming, dependency injection, async lifecycle, error taxonomy, contract tests, load/failure tests | **High** |
| 4 | LLM Application Foundations | provider abstraction, structured outputs, model routing, fallback, capability matrix, deterministic post-processing, model failure simulation | **High** |
| 5 | Prompting + Evaluation | prompt anatomy, constraints, few-shot, decomposition, structured output, prompt versioning, eval datasets, judge calibration, regression | **High** |

### RAG engineering: Modules 6–12

| # | Module | Required practical emphasis | QA priority |
|---|---|---|---|
| 6 | RAG From First Principles | document→chunk→embed→index→retrieve→context→answer, cosine similarity, chunk-size experiments, ACL filtering, abstention | **Critical** |
| 7 | Embeddings + Vector DB | vector geometry, embedding quality, exact vs ANN, HNSW/IVF concepts, metadata filters, Recall@K, versioning, migration | **Critical** |
| 8 | Document Intelligence + PII | parsing, structure recovery, tables, OCR concepts, normalization, PII detection/redaction, provenance, adversarial documents | **Critical** |
| 9 | Advanced Retrieval | lexical/BM25, dense retrieval, hybrid/RRF, reranking, query transformation, multi-query, compression, ACL-aware retrieval | **Critical** |
| 10 | RAG Optimization | caching, invalidation, context budgets, latency/cost profiling, incremental ingestion, versioning, shadow/canary/rollback | **High** |
| 11 | RAG Evaluation | golden datasets, Recall/MRR/nDCG, groundedness, citation correctness, judge calibration, confidence intervals, regression gates | **Critical** |
| 12 | RAG Debugging | trace-first debugging, retrieval miss, bad chunk, wrong filter, generation failure, latency/cost/security diagnosis, incident→regression | **Critical** |

### Agent engineering: Modules 13–18

| # | Module | Required practical emphasis | QA priority |
|---|---|---|---|
| 13 | Tool Calling + API Agents | JSON schema, tool registry, validation, RBAC, risk classes, approval, idempotency, retries/timeouts, malicious tool outputs | **Critical** |
| 14 | Raw Agent Loop | OBSERVE→DECIDE→ACT→VERIFY→RECOVER, termination, budgets, repeated-state detection, trajectory capture, no-framework implementation | **Critical** |
| 15 | Memory | working/episodic/semantic/procedural/user/task memory, provenance, contradiction, TTL, poisoning, tenant isolation | **Critical** |
| 16 | LangGraph Stateful Workflows | state schema, nodes, routers, checkpoints, interrupts, reducers, subgraphs, replay/time travel, cancellation, deadlines | **High** |
| 17 | Planning + Human-in-the-Loop | planner/executor/verifier, pre/postconditions, replanning, exact approval binding, risk-aware plans, partial completion | **Critical** |
| 18 | Agent Security | direct/indirect prompt injection, tool poisoning, memory poisoning, confused deputy, SSRF, secret leakage, authorization, audit | **Critical** |

### Multi-agent + MCP: Modules 19–24

| # | Module | Required practical emphasis | QA priority |
|---|---|---|---|
| 19 | Multi-Agent Reality Check | baseline single-agent comparison, coordination cost, latency, security, measured success gain, architecture selection | **Critical** |
| 20 | Multi-Agent Architectures | supervisor/worker, typed envelopes, routing, fan-out/fan-in, partial failure, deadlines, idempotency, contract enforcement | **Critical** |
| 21 | Coordination + Fault Tolerance | message envelopes, leases, heartbeats, duplicate/out-of-order delivery, retry taxonomy, backpressure, dead-letter, recovery | **Critical** |
| 22 | Multi-Agent Debugging | distributed traces, causality, first failure, replay, differential debugging, cost attribution, security-event correlation | **Critical** |
| 23 | MCP Fundamentals | host/client/server model, capability discovery, tools/resources/prompts, schemas, trust boundaries, tenant binding | **High** |
| 24 | Enterprise MCP Server | authentication, authorization, capability catalog, action hashes, high-risk mutation controls, idempotency, audit | **Critical** |

### Production engineering: Modules 25–30

| # | Module | Required practical emphasis | QA priority |
|---|---|---|---|
| 25 | Observability | traces/spans/events/metrics, critical path, token/cost attribution, quality correlation, retry amplification, tenant-safe telemetry | **Critical** |
| 26 | Production Evaluation | golden cases, A/B, shadow, regression gates, confidence intervals, slice analysis, safety/cost/latency release criteria | **Critical** |
| 27 | Cost Engineering | token/tool/compute/storage costs, cost/success, budgets, cascades, caching, retry economics, tenant chargeback | **High** |
| 28 | Responsible AI + Governance | risk classification, policy precedence, privacy/data class, human oversight, approval, audit, remediation, re-evaluation | **Critical** |
| 29 | Deployment + CI/CD | reproducible builds, immutable artifacts, model/prompt/RAG/tool versioning, evaluation/governance gates, shadow/canary/rollback | **Critical** |
| 30 | AegisAI Capstone | complete enterprise Agentic RAG, integration, security, durability, evaluation, economics, deployment and evidence pack | **Critical** |

### Frontier agent engineering: Modules 31–38

| # | Module | Required practical emphasis | QA priority |
|---|---|---|---|
| 31 | Loop Engineering | explicit loop ownership, halting, budgets, recovery, verifier control, trajectory and loop pathology | **Critical** |
| 32 | Harness Engineering | model+harness separation, context management, tool gateway, policy, state, verification, extension surface, replay | **Critical** |
| 33 | Long-Running Autonomous Agents | durable goals/tasks/runs, leases, checkpoints, waiting states, idempotency, approval persistence, revocation, scheduled autonomy | **Critical** |
| 34 | Skills, Memory + Continual Harnesses | candidate vs trusted assets, provenance, skill extraction, validation, versioning, poisoning, rollback, continual evaluation | **Critical** |
| 35 | Environments, Verifiers + Agentic RL | task generation, environment contracts, deterministic verifiers, reward design, rollout collection, reward hacking, held-out eval | **Critical** |
| 36 | Recursive / Self-Improving Agents | baseline→proposal→experiment→verify→gate→deploy→monitor→rollback, recursion limits, contamination, evaluator gaming | **Critical** |
| 37 | Computer Use + Always-On AI Teammates | screen/DOM state, action grounding, policy/approval, stale state, secret boundary, verification, scheduling, audit | **Critical** |
| 38 | Frontier Agentic RAG Capstone | integrate all frontier primitives into durable, governed, verified autonomous enterprise workflows | **Critical** |

## Required Google Colab notebook contract

Every module notebook should be upgraded toward this exact structure:

1. **Prerequisites and learning objectives**
2. **Concept map**
3. **Why the concept exists**
4. **Smallest runnable example**
5. **Mechanism from first principles**
6. **Visualization / architecture diagram**
7. **Industry scenario**
8. **Guided Lab A**
9. **Guided Lab B**
10. **Experiment matrix**
11. **Failure injection**
12. **Debugging challenge**
13. **Measurement and metrics**
14. **Optimization challenge**
15. **Security / misuse challenge**
16. **Independent coding challenge**
17. **System-design challenge**
18. **Hints**
19. **Reference solution**
20. **Expected observations / outputs**
21. **Reflection questions**
22. **Mastery gate**

### Colab design rules

- Prefer standard Python and lightweight packages first.
- Use synthetic/local datasets by default.
- Do not require API keys for core learning.
- Clearly mark optional provider integrations.
- Every important code cell should have a learning question attached.
- Include both a working implementation and an intentionally broken implementation.
- Make expected output deterministic wherever practical.
- Include reset/re-run instructions.
- Include tests or assertions in the notebook.
- Separate **student TODO cells** from **reference solution cells**.
- Never hide the solution inside an unexplained magic function.

## Solution standard

For every major exercise, the solution should contain:

```text
Problem interpretation
→ constraints
→ design choice
→ implementation
→ test
→ expected result
→ failure analysis
→ production improvement
```

A solution that only prints the answer is insufficient.

## Industry scenario standard

Across the 38 modules, examples should deliberately rotate through:

- Banking / payments / reconciliation
- Healthcare / clinical-document workflows
- Cybersecurity / SOC / incident response
- Manufacturing / predictive maintenance / quality
- Enterprise IT / SRE / service management
- E-commerce / procurement / customer operations
- Legal / policy / contract analysis
- Software engineering / coding teammates
- Sales / research / enterprise knowledge work

High-risk scenarios must use synthetic data and must teach authorization, approval and verification rather than unrestricted real-world execution.

## Cross-module progression

```text
01 Architecture
   ↓
02–05 AI application engineering
   ↓
06–12 RAG engineering
   ↓
13–18 Tool + agent engineering
   ↓
19–24 Multi-agent + MCP
   ↓
25–30 Production engineering
   ↓
31 Loop engineering
   ↓
32 Harness engineering
   ↓
33 Durable autonomy
   ↓
34 Memory + skills + continual learning
   ↓
35 Environments + verifiers + agentic RL
   ↓
36 Recursive improvement
   ↓
37 Computer use / always-on workers
   ↓
38 Frontier AegisAI platform
```

## Cross-module mastery requirements

A learner should repeatedly demonstrate seven levels:

- **L1:** explain
- **L2:** implement
- **L3:** debug
- **L4:** measure and optimize
- **L5:** design production architecture
- **L6:** defend trade-offs
- **L7:** solve an unfamiliar scenario

The later modules should not simply repeat earlier labs with a different framework. Each should add a new systems constraint.

## Critical QA findings to resolve

### 1. Notebook depth

Notebook presence is currently strong, but several early notebooks are compact relative to the desired deep-practice standard. They need more worked code, TODO cells, failure injection, measurements and reference solutions.

### 2. Supporting learning artifacts

Module 1 already demonstrates the desired richer organization with theory, diagrams, exercises, labs, tests, assessment and interview material. Many modules currently rely more heavily on README/app/tests/notebook. The richer artifact structure should be progressively normalized.

### 3. Module 6 duplicate

Two directories exist:

- `06-rag-first-principles`
- `06-rag-from-first-principles`

Do not discard either until their README, implementation, tests and learning material are compared. The final course should have one canonical Module 6 with the best material merged.

### 4. Frontier module consistency

Modules 31–38 have strong conceptual README material and substantial Colab lab packs, but the same depth of independent exercises, reference solutions and automated assessment should be made consistent across all eight modules.

### 5. Executability QA

Repository presence is verified. Full execution of every notebook and every module test suite still requires a dedicated runtime/CI validation pass. Do not label all notebooks as execution-tested until that pass has actually run.

## Definition of done for the entire course

The course is considered **complete** only when every module has:

- coherent theory
- concept map
- architecture/data/control diagrams
- implementation walkthrough
- runnable lab
- at least one realistic industry scenario
- failure-first lab
- measurable experiment
- security consideration
- independent coding challenge
- debugging challenge
- system-design challenge
- Colab practice notebook
- hints + reference solutions
- tests/assertions
- interview questions
- mastery gate
- explicit links to prerequisite and successor modules

The goal is not 38 folders. The goal is a **progressive engineering apprenticeship** in which every module forces the learner to build, break, measure, explain and defend an AI system.