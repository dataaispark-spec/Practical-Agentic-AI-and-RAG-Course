# Module Deep-Practice Implementation Pack — Modules 1–38

This pack operationalizes the course QA standard. It is intentionally module-specific: existing strong material is retained; missing depth is added through explicit BUILD / TRY / BREAK / MEASURE / DEFEND work.

## Completion rule

A module is not considered practice-complete merely because a notebook exists. The learner must be able to **explain → build → break → debug → measure → optimize → defend** the mechanism.

Every module below must have these notebook elements, either in the canonical Colab notebook or in linked companion material:

1. prerequisites + objectives
2. concept map
3. first-principles theory
4. smallest runnable example
5. architecture/data/control-flow diagram
6. guided implementation
7. industry scenario
8. two guided labs
9. experiment matrix
10. student TODO
11. intentionally broken version
12. debugging challenge
13. metrics/evaluation
14. optimization challenge
15. security/misuse challenge
16. independent coding challenge
17. system-design challenge
18. hints
19. reference solution with reasoning + tests
20. expected observations
21. reflection
22. mastery gate

## Module-by-module implementation targets

### 01 — AI Systems Thinking & Architecture Decisions
**Industry lab:** enterprise knowledge assistant where the learner must choose workflow, RAG, agent, or multi-agent architecture.
**BUILD:** requirements decomposition and architecture scoring.
**TRY:** change latency, risk, data sensitivity, and actionability constraints and recompute the recommendation.
**BREAK:** remove a hard constraint and force an unsafe/over-complex recommendation; diagnose the decision error.
**MEASURE:** expected success, latency, cost, risk, operational complexity.
**DEFEND:** write an ADR explaining why the minimum sufficient architecture wins.
**Gold:** design two competing architectures and reject one with evidence.

### 02 — Python for AI Engineering
**Industry lab:** resilient async model gateway.
**BUILD:** typed request/response models, timeout, semaphore, retry/backoff, cancellation and structured errors.
**TRY:** implement bounded concurrency and cancellation propagation.
**BREAK:** inject timeout, provider failure, malformed response and retry storm.
**MEASURE:** throughput, p95 latency, retry amplification, failure rate.
**DEFEND:** explain why cancellation and idempotency matter in AI services.
**Gold:** add a deterministic fake provider and a property-oriented test matrix.

### 03 — FastAPI + Testing
**Industry lab:** streaming enterprise AI endpoint.
**BUILD:** typed API contract, validation, dependency injection, streaming and error taxonomy.
**TRY:** add request correlation and a fake provider.
**BREAK:** malformed input, provider timeout, client disconnect and partial stream failure.
**MEASURE:** p50/p95 latency, error classes, stream completion rate.
**DEFEND:** distinguish unit, contract, integration and load/failure tests.
**Gold:** produce a production API test strategy without requiring an external LLM.

### 04 — LLM Application Foundations
**Industry lab:** model router for enterprise support.
**BUILD:** provider abstraction, capability matrix, structured output and deterministic post-processing.
**TRY:** implement quality/privacy/cost/latency routing constraints.
**BREAK:** provider outage, invalid JSON, capability mismatch and stale health state.
**MEASURE:** task success, fallback rate, latency and cost/request.
**DEFEND:** explain why routing must be deterministic even when model behavior is probabilistic.
**Gold:** design a shadow router and rollback rule.

### 05 — Prompting + Evaluation
**Industry lab:** policy-answering assistant.
**BUILD:** prompt anatomy, constraints, examples and structured output.
**TRY:** create competing prompt versions and an evaluation set.
**BREAK:** prompt injection, format drift, unsupported claims and evaluator bias.
**MEASURE:** task success, format validity, groundedness and regression delta.
**DEFEND:** explain judge calibration and why prompt changes need regression tests.
**Gold:** implement a small prompt regression harness.

### 06 — RAG From First Principles
**Industry lab:** synthetic banking policy corpus.
**BUILD:** document → chunk → embedding → index → retrieval → context → answer/abstain.
**TRY:** vary chunk size, overlap and top-k.
**BREAK:** irrelevant chunks, wrong tenant, missing evidence and poisoned text.
**MEASURE:** Recall@K, evidence coverage, abstention precision, latency.
**DEFEND:** explain cosine similarity and why retrieval errors propagate into generation.
**Gold:** compare at least three chunking strategies and select one with evidence.

### 07 — Embeddings + Vector DB
**Industry lab:** multi-tenant enterprise semantic search.
**BUILD:** vector geometry, exact search and metadata filtering.
**TRY:** benchmark exact vs simulated ANN behavior.
**BREAK:** dimension mismatch, stale embedding version, ACL leakage and poor recall.
**MEASURE:** Recall@K, query latency, index size and migration cost.
**DEFEND:** explain HNSW/IVF trade-offs without treating a vector DB as magic.
**Gold:** design an embedding-version migration and rollback plan.

### 08 — Document Intelligence + PII
**Industry lab:** synthetic healthcare document pipeline.
**BUILD:** parsing, normalization, structure recovery, PII detection/redaction and provenance.
**TRY:** preserve page/section/source lineage through transformations.
**BREAK:** malformed document, table loss, OCR uncertainty, PII miss and adversarial instructions.
**MEASURE:** extraction accuracy, PII recall, provenance coverage and processing latency.
**DEFEND:** distinguish source truth from transformed text.
**Gold:** design an adversarial document test suite.

### 09 — Advanced Retrieval
**Industry lab:** legal/contract retrieval.
**BUILD:** lexical, dense, hybrid/RRF and reranking pipelines.
**TRY:** tune candidate depth and reranker budget.
**BREAK:** lexical-only miss, dense semantic miss, duplicated evidence and ACL mismatch.
**MEASURE:** Recall@K, MRR/nDCG, reranker lift, latency and cost.
**DEFEND:** explain when hybrid retrieval beats simply increasing top-k.
**Gold:** run an ablation study across retrieval stages.

### 10 — RAG Optimization
**Industry lab:** high-volume enterprise knowledge platform.
**BUILD:** caching, invalidation, context budgets and versioned ingestion.
**TRY:** create cache keys that include tenant and knowledge version.
**BREAK:** stale cache, invalidation miss, context explosion and bad canary.
**MEASURE:** cache hit rate, p95 latency, cost/request and freshness lag.
**DEFEND:** explain shadow, canary and rollback for retrieval changes.
**Gold:** produce a cost/latency/quality optimization report.

### 11 — RAG Evaluation
**Industry lab:** release gate for a regulated knowledge assistant.
**BUILD:** golden cases, retrieval metrics, groundedness, citation correctness and regression gates.
**TRY:** add confidence intervals and slice analysis.
**BREAK:** leaked answers, duplicate cases, cherry-picked evaluation and judge drift.
**MEASURE:** Recall@K, MRR/nDCG, groundedness, safety, latency and cost/success.
**DEFEND:** explain why averages alone are insufficient.
**Gold:** block a release using an evidence-based gate.

### 12 — RAG Debugging
**Industry lab:** incident investigation for an enterprise assistant.
**BUILD:** trace-first debugging and first-failure classification.
**TRY:** reconstruct an incident from trace events.
**BREAK:** retrieval miss, bad filter, generation failure, timeout and security event.
**MEASURE:** time-to-diagnosis, first-failure accuracy, latency/cost attribution.
**DEFEND:** distinguish symptom from root cause.
**Gold:** convert an incident into a permanent regression test.

### 13 — Tool Calling + API Agents
**Industry lab:** synthetic enterprise service-management agent.
**BUILD:** JSON schema, registry, RBAC, risk classes, approval and idempotency.
**TRY:** add retries/timeouts and tool-result validation.
**BREAK:** malformed arguments, malicious output, unauthorized tool, duplicate mutation.
**MEASURE:** tool success, policy-denial rate, duplicate-effect rate, latency and cost.
**DEFEND:** explain why tool output is untrusted data.
**Gold:** implement exact-action approval binding.

### 14 — Raw Agent Loop
**Industry lab:** framework-free incident triage agent.
**BUILD:** OBSERVE → DECIDE → ACT → VERIFY → RECOVER/STOP.
**TRY:** add hard step/token/tool budgets and repeated-state detection.
**BREAK:** infinite loop, oscillation, false verification, duplicate action and stale observation.
**MEASURE:** task success, steps/task, recovery rate, loop amplification and cost.
**DEFEND:** identify which decisions belong to the model and which belong to deterministic control code.
**Gold:** implement replayable trajectory capture.

### 15 — Memory
**Industry lab:** enterprise support agent with tenant-scoped memory.
**BUILD:** working, episodic, semantic, procedural, user and task memory.
**TRY:** provenance, confidence, importance, contradiction and supersession.
**BREAK:** poisoned memory, stale preference, tenant leakage and permission drift.
**MEASURE:** retrieval usefulness, contradiction rate, stale-memory rate and storage growth.
**DEFEND:** explain why persistence changes the threat model.
**Gold:** implement gated memory promotion and forgetting.

### 16 — LangGraph Stateful Workflows
**Industry lab:** approval workflow with recoverable state.
**BUILD:** typed state, nodes, routers and checkpoints.
**TRY:** conditional edges, reducers, parallel branches and interrupts.
**BREAK:** stale state, duplicate branch, cancellation, deadline and replay inconsistency.
**MEASURE:** completion rate, recovery rate, state transition validity and latency.
**DEFEND:** explain framework abstraction versus underlying state-machine mechanics.
**Gold:** replay a failed run and identify the first divergent state.

### 17 — Planning + Human-in-the-Loop
**Industry lab:** synthetic procurement approval workflow.
**BUILD:** planner/executor/verifier with preconditions and postconditions.
**TRY:** add adaptive replanning and risk-aware approval.
**BREAK:** cyclic plan, stale approval, partial completion and mismatched high-risk action.
**MEASURE:** plan validity, completion rate, human escalation, cost and time-to-completion.
**DEFEND:** explain why approval should bind to the exact action, not merely the goal.
**Gold:** design a plan verifier independent from the planner.

### 18 — Agent Security
**Industry lab:** synthetic SOC investigation agent.
**BUILD:** trust labels, policy engine, authorization, approval, egress controls and audit.
**TRY:** red-team direct/indirect injection and tool poisoning.
**BREAK:** confused deputy, SSRF-style request, secret leakage, cross-tenant access and replay.
**MEASURE:** attack success rate, policy coverage, false-positive rate and audit completeness.
**DEFEND:** explain security invariants that model output must never override.
**Gold:** produce a threat model + control mapping.

### 19 — Multi-Agent Reality Check
**Industry lab:** compare one analyst agent against specialist workers for incident analysis.
**BUILD:** single-agent baseline first.
**TRY:** score success gain against cost, latency, coordination and security risk.
**BREAK:** correlated worker failures and coordination overhead.
**MEASURE:** success gain, cost/success, p95 latency and disagreement rate.
**DEFEND:** reject multi-agent architecture when measured gain is insufficient.
**Gold:** write an architecture decision backed by benchmark data.

### 20 — Multi-Agent Architectures
**Industry lab:** supervisor/worker enterprise research system.
**BUILD:** typed task envelopes, worker registry and fan-out/fan-in.
**TRY:** deadlines, idempotency and partial failure handling.
**BREAK:** duplicate delivery, expired task, capability escalation and invalid result.
**MEASURE:** worker utilization, partial-success rate, coordination latency and duplicate effects.
**DEFEND:** explain contract enforcement at every delegation boundary.
**Gold:** design a supervisor that cannot grant capabilities it does not possess.

### 21 — Coordination + Fault Tolerance
**Industry lab:** distributed enterprise agent network.
**BUILD:** message envelope, leases, heartbeat and retry taxonomy.
**TRY:** backpressure, dead-letter and recovery.
**BREAK:** stale worker, lost heartbeat, duplicate/out-of-order delivery and partition.
**MEASURE:** recovery time, duplicate-effect rate, queue depth and retry amplification.
**DEFEND:** distinguish transient, permanent, authorization and timeout failures.
**Gold:** chaos-test coordinator recovery without duplicate side effects.

### 22 — Multi-Agent Debugging
**Industry lab:** distributed agent incident trace.
**BUILD:** causal trace across supervisor, workers, messages, retrieval, tools and verifier.
**TRY:** first-failure detection and replay.
**BREAK:** race, aggregation error, retrieval poisoning and policy denial.
**MEASURE:** first-failure accuracy, causal-chain completeness and cost attribution.
**DEFEND:** explain why root-cause analysis must follow causality rather than event order alone.
**Gold:** differential-debug two trajectories and isolate the divergent component.

### 23 — MCP Fundamentals
**Industry lab:** synthetic enterprise capability client.
**BUILD:** host/client/server model, discovery and typed tool calls.
**TRY:** resources/prompts, tenant binding and trust labels.
**BREAK:** unauthorized capability, malicious result and schema mismatch.
**MEASURE:** capability discovery correctness, policy-denial rate and call latency.
**DEFEND:** explain why MCP is a capability/context interface, not an authorization system.
**Gold:** design the client-side trust boundary.

### 24 — Enterprise MCP Server
**Industry lab:** governed enterprise capability gateway.
**BUILD:** authentication, authorization, capability catalog and audit.
**TRY:** canonical action hashes and high-risk mutation controls.
**BREAK:** missing idempotency key, cross-role access, replay and malicious parameters.
**MEASURE:** authorization coverage, mutation duplicate rate and audit completeness.
**DEFEND:** explain canonical action identity and replay protection.
**Gold:** design a fail-closed enterprise MCP gateway.

### 25 — Observability
**Industry lab:** AegisAI telemetry control plane.
**BUILD:** traces, spans, events and metrics across model/RAG/tool/MCP layers.
**TRY:** critical-path and cost attribution.
**BREAK:** missing parent span, clock skew, dropped security event, retry storm and tenant leak.
**MEASURE:** telemetry coverage, trace completeness, p95 latency and cost attribution accuracy.
**DEFEND:** correlate quality with operational telemetry.
**Gold:** build an incident dashboard specification.

### 26 — Production Evaluation
**Industry lab:** release certification for an enterprise agent.
**BUILD:** golden cases and multidimensional release gate.
**TRY:** A/B, shadow, confidence intervals and slice analysis.
**BREAK:** cherry-picking, tiny samples, judge bias and quality/safety trade-off regression.
**MEASURE:** task success, safety, groundedness, latency and cost/success.
**DEFEND:** define BLOCK/WARN/PASS criteria.
**Gold:** certify or block a release and justify every gate.

### 27 — Cost Engineering
**Industry lab:** cost-aware enterprise agent router.
**BUILD:** full cost ledger: model, embeddings, reranking, tools, storage, compute and human review.
**TRY:** budget-aware cascades and caching.
**BREAK:** retry amplification, loop explosion and cheap-but-unauthorized provider routing.
**MEASURE:** cost/request, cost/success, quality-adjusted cost and budget utilization.
**DEFEND:** optimize under quality, latency and security constraints simultaneously.
**Gold:** construct a cost-quality frontier.

### 28 — Responsible AI + Governance
**Industry lab:** synthetic regulated workflow.
**BUILD:** risk classification, data class, model/tool eligibility, oversight and audit.
**TRY:** policy precedence and remediation workflow.
**BREAK:** bypassed approval, forbidden data class and policy conflict.
**MEASURE:** policy coverage, approval compliance, audit completeness and remediation time.
**DEFEND:** distinguish educational governance controls from legal advice or jurisdiction-specific requirements.
**Gold:** turn a policy requirement into executable controls.

### 29 — Deployment + CI/CD
**Industry lab:** production release pipeline for AegisAI.
**BUILD:** immutable artifact and release manifest.
**TRY:** model/prompt/RAG/tool/policy version gates, shadow and canary.
**BREAK:** missing manifest field, failed evaluation gate and rollback mismatch.
**MEASURE:** deployment lead time, change failure rate, rollback time and gate accuracy.
**DEFEND:** explain why AI release identity includes more than application code.
**Gold:** design a reversible release process.

### 30 — AegisAI Capstone
**Industry lab:** complete synthetic enterprise Agentic RAG platform.
**BUILD:** API → contract → policy/security/budget → agent → RAG/memory/tools/MCP → verification → telemetry/evaluation → durable execution.
**TRY:** add HITL, crash recovery and release controls.
**BREAK:** injected retrieval miss, tool failure, policy denial, worker crash and budget exhaustion.
**MEASURE:** task success, groundedness, citation correctness, safety, recovery, p95 latency and cost/success.
**DEFEND:** present architecture, evidence and trade-offs.
**Gold:** produce a portfolio-ready evidence pack.

### 31 — Loop Engineering
**Industry lab:** production loop engine.
**BUILD:** explicit loop ownership and state transitions.
**TRY:** halting, budgets, verifier and recovery policies.
**BREAK:** infinite loop, retry storm, oscillation and false success.
**MEASURE:** steps/task, loop amplification, recovery rate and cost.
**DEFEND:** identify control-plane invariants.
**Gold:** compare two loop policies using identical model decisions.

### 32 — Harness Engineering
**Industry lab:** reusable AegisAI agent harness.
**BUILD:** model adapter, context manager, tool gateway, policy, state, budget, verification and telemetry.
**TRY:** swap model/provider without changing governance.
**BREAK:** context ordering, tool validation, checkpoint restore and tenant isolation.
**MEASURE:** harness overhead, task success, replay determinism and policy coverage.
**DEFEND:** explain why the harness is part of the agent system rather than plumbing.
**Gold:** create a stable harness contract across model versions.

### 33 — Long-Running Autonomous Agents
**Industry lab:** durable enterprise worker.
**BUILD:** goal/task/run records, checkpoints, leases, heartbeat and waiting states.
**TRY:** scheduled wake-up, approval wait and restart recovery.
**BREAK:** crash during mutation, stale worker, expired approval and provider outage.
**MEASURE:** recovery rate, duplicate effects, uptime, cost/run and SLA adherence.
**DEFEND:** explain what state must survive process restart.
**Gold:** prove stop/restart/resume safety.

### 34 — Skills, Memory + Continual Harnesses
**Industry lab:** synthetic self-improving support worker.
**BUILD:** trajectory → candidate skill/memory → validation → version → deployment.
**TRY:** provenance, contradiction and forgetting.
**BREAK:** poisoned memory, unsafe skill, benchmark overfit and silent overwrite.
**MEASURE:** improvement delta, regression rate, stale-memory rate and promotion rejection rate.
**DEFEND:** distinguish candidate assets from trusted assets.
**Gold:** implement rollback for a harmful learned skill.

### 35 — Environments, Verifiers + Agentic RL
**Industry lab:** synthetic task environment for enterprise workflows.
**BUILD:** task generator, environment state, action contract and deterministic verifier.
**TRY:** reward decomposition and trajectory collection.
**BREAK:** reward hacking, verifier gaming, leaked tasks and distribution shift.
**MEASURE:** verified success, reward/verifier correlation, held-out performance and safety violations.
**DEFEND:** explain why reward is not automatically ground truth.
**Gold:** build a held-out benchmark the agent cannot trivially game.

### 36 — Recursive / Self-Improving Agents
**Industry lab:** controlled harness improvement loop.
**BUILD:** baseline → proposal → experiment → verify → gate → deploy → monitor → rollback.
**TRY:** mutate prompt, retrieval, skill or harness component under a budget.
**BREAK:** evaluator gaming, contamination, runaway recursion and safety regression.
**MEASURE:** paired improvement, safety delta, experiment cost and rollback success.
**DEFEND:** explain external promotion gates.
**Gold:** run competing improvements and promote only the evidence-backed candidate.

### 37 — Computer Use + Always-On AI Teammates
**Industry lab:** synthetic browser-based enterprise worker.
**BUILD:** observe state → propose action → policy → approval → execute → verify → evidence.
**TRY:** screen/DOM grounding, scheduling and interruption handling.
**BREAK:** stale screen, hostile page, wrong click, duplicate submission and secret exposure.
**MEASURE:** action accuracy, unsafe-action block rate, recovery and cost/hour.
**DEFEND:** explain why visual confidence is not authorization.
**Gold:** build a safe always-on worker with durable audit.

### 38 — Frontier Agentic RAG Capstone
**Industry lab:** complete autonomous enterprise teammate using synthetic data and tools.
**BUILD:** model + harness + environment + tools + state + policy + verification + evaluation + improvement.
**TRY:** combine RAG, memory, MCP, durable execution, computer use and multi-agent escalation.
**BREAK:** coordinated failures across retrieval, tools, state, policy and verifier.
**MEASURE:** task success, groundedness, citation correctness, verifier pass, safety violations, recovery, p95 latency and cost/success.
**DEFEND:** explain every control boundary and every rollback path.
**Gold:** pass a full chaos benchmark and produce architecture/evaluation/security evidence.

## Cross-module experiment matrix

Use the same synthetic business scenario family through the course so the learner sees systems mature rather than restarting from toy examples:

| Stage | Primary experiment |
|---|---|
| 1–5 | architecture, provider, prompt and service reliability |
| 6–12 | retrieval quality, evidence, optimization and debugging |
| 13–18 | tools, loops, memory, planning and security |
| 19–24 | coordination, multi-agent economics and MCP boundaries |
| 25–30 | observability, evaluation, cost, governance and deployment |
| 31–34 | loop/harness durability, memory and continual skills |
| 35–36 | verified environments, rewards and controlled improvement |
| 37 | computer-use safety and always-on operation |
| 38 | end-to-end frontier autonomy under hard controls |

## Reference-solution policy

Every independent challenge must have a solution path, not just an answer:

**Interpretation → constraints → design → implementation → test → expected result → failure analysis → production improvement → trade-offs.**

## Definition of an audit-complete module

A module can be marked `COMPLETE` only when its actual repository evidence satisfies the course QA checker and the learner can demonstrate L1–L7 capability. Existing content should be reused; duplicated content should not be created merely to inflate file counts.
