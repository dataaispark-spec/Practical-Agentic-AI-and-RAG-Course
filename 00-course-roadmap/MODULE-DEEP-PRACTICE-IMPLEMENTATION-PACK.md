# Module Deep-Practice Implementation Pack — Modules 01–43

**Status:** normative module-specific practice targets  
**Canonical branch:** `main`  
**Updated:** 2026-09-09

This pack operationalizes the course engineering standard at module level. It is intentionally specific: each module gets a distinct systems problem, failure class and measurable outcome. It must be read together with [`COURSE-ENGINEERING-STANDARDS.md`](./COURSE-ENGINEERING-STANDARDS.md) and [`COLAB-PRACTICE-NOTEBOOK-STANDARD.md`](./COLAB-PRACTICE-NOTEBOOK-STANDARD.md).

## Module practice contract

Every module must provide evidence for the following, scaled to the topic:

1. prerequisites + objectives;
2. concept map;
3. first-principles mechanism;
4. smallest runnable example;
5. architecture/data/control-flow representation;
6. guided implementation;
7. realistic synthetic industry scenario;
8. guided experiments;
9. student TODO / independent work;
10. intentional failure;
11. debugging;
12. measurement;
13. optimization/trade-off analysis;
14. security/misuse analysis where relevant;
15. system-design challenge;
16. hints;
17. reference solution with reasoning/tests;
18. expected observations;
19. reflection;
20. mastery gate.

Do not manufacture extra prose or repeated labs just to satisfy this checklist.

## Module-specific targets

### 01 — AI Systems Thinking & Architecture Decisions
**Scenario:** enterprise knowledge assistant.  
**BUILD:** requirements decomposition and architecture scoring.  
**TRY:** vary latency, risk, sensitivity and actionability constraints.  
**BREAK:** force an unsafe/over-complex recommendation by removing a hard constraint.  
**MEASURE:** expected success, latency, cost, risk, operational complexity.  
**DEFEND:** ADR for the minimum sufficient architecture.  
**Gold:** compare two viable architectures and reject one with evidence.

### 02 — Python for AI Engineering
**Scenario:** resilient async model gateway.  
**BUILD:** typed contracts, async concurrency, cancellation, timeout, retry/backoff and structured errors.  
**TRY:** implement bounded concurrency and cancellation propagation.  
**BREAK:** timeout, provider failure, malformed response and retry storm.  
**MEASURE:** throughput, p95 latency, retry amplification, failure rate.  
**DEFEND:** cancellation/idempotency rationale.  
**Gold:** deterministic fake provider + property-oriented test matrix.

### 03 — FastAPI + Testing
**Scenario:** streaming enterprise AI endpoint.  
**BUILD:** typed API, validation, DI, streaming and error taxonomy.  
**TRY:** correlation IDs and fake provider.  
**BREAK:** malformed input, provider timeout, disconnect and partial stream failure.  
**MEASURE:** p50/p95 latency, error classes, stream completion.  
**DEFEND:** unit vs contract vs integration vs failure/load testing.  
**Gold:** production API test strategy without external LLM dependency.

### 04 — LLM Application Foundations
**Scenario:** enterprise support model router.  
**BUILD:** provider abstraction, capability matrix, structured output, deterministic post-processing.  
**TRY:** quality/privacy/cost/latency routing constraints.  
**BREAK:** outage, invalid JSON, capability mismatch, stale health.  
**MEASURE:** success, fallback rate, latency, cost/request.  
**DEFEND:** deterministic control around probabilistic model choice.  
**Gold:** shadow router + rollback rule.

### 05 — Prompting + Evaluation
**Scenario:** policy-answering assistant.  
**BUILD:** prompt anatomy, constraints, examples, structured output and evaluation set.  
**TRY:** competing prompt versions + regression harness.  
**BREAK:** injection, format drift, unsupported claims, evaluator bias.  
**MEASURE:** task success, format validity, groundedness, regression delta.  
**DEFEND:** judge calibration and prompt regression rationale.  
**Gold:** small reproducible prompt-evaluation harness.

### 06 — RAG From First Principles
**Scenario:** synthetic banking-policy corpus.  
**BUILD:** document→chunk→embed→index→retrieve→context→answer/abstain.  
**TRY:** chunk size, overlap, top-k.  
**BREAK:** irrelevant evidence, wrong tenant, missing evidence, poisoned text.  
**MEASURE:** Recall@K, evidence coverage, abstention quality, latency.  
**DEFEND:** retrieval-to-generation error propagation.  
**Gold:** compare three chunking strategies with evidence.

### 07 — Embeddings + Vector DB
**Scenario:** multi-tenant semantic search.  
**BUILD:** vector geometry, exact search, metadata filtering.  
**TRY:** exact vs simulated ANN behavior and embedding versions.  
**BREAK:** dimension mismatch, stale embedding, ACL leakage, recall loss.  
**MEASURE:** Recall@K, latency, index size, migration cost.  
**DEFEND:** HNSW/IVF trade-offs.  
**Gold:** version migration + rollback plan.

### 08 — Document Intelligence + PII
**Scenario:** synthetic healthcare documents.  
**BUILD:** parsing, normalization, structure recovery, PII detection/redaction, provenance.  
**TRY:** preserve lineage through transformations.  
**BREAK:** malformed document, table loss, OCR uncertainty, PII miss, adversarial instructions.  
**MEASURE:** extraction accuracy, PII recall, provenance coverage, latency.  
**DEFEND:** source truth vs transformed text.  
**Gold:** adversarial document test suite.

### 09 — Advanced Retrieval
**Scenario:** legal/contract retrieval.  
**BUILD:** lexical, dense, hybrid/RRF and reranking.  
**TRY:** candidate depth and reranker budget.  
**BREAK:** lexical/dense miss, duplication, ACL mismatch.  
**MEASURE:** Recall@K, MRR/nDCG, reranker lift, latency, cost.  
**DEFEND:** when hybrid beats simply increasing top-k.  
**Gold:** retrieval-stage ablation study.

### 10 — RAG Optimization
**Scenario:** high-volume knowledge platform.  
**BUILD:** caching, invalidation, context budgets, versioned ingestion.  
**TRY:** tenant + knowledge-version cache key.  
**BREAK:** stale cache, invalidation miss, context explosion, bad canary.  
**MEASURE:** hit rate, p95 latency, cost/request, freshness lag.  
**DEFEND:** shadow/canary/rollback.  
**Gold:** optimization report balancing quality, latency and cost.

### 11 — RAG Evaluation
**Scenario:** regulated knowledge-assistant release gate.  
**BUILD:** golden set, retrieval metrics, groundedness, citation correctness and regressions.  
**TRY:** confidence intervals and slice analysis.  
**BREAK:** leakage, duplicate cases, cherry-picking, judge drift.  
**MEASURE:** Recall@K, MRR/nDCG, grounding, safety, latency, cost/success.  
**DEFEND:** why averages are insufficient.  
**Gold:** block a release using evidence.

### 12 — RAG Debugging
**Scenario:** enterprise assistant incident.  
**BUILD:** trace-first debugging and first-failure classification.  
**TRY:** reconstruct incident from trace events.  
**BREAK:** retrieval miss, filter bug, generation error, timeout, security event.  
**MEASURE:** time-to-diagnosis, first-failure accuracy, latency/cost attribution.  
**DEFEND:** symptom vs root cause.  
**Gold:** turn the incident into a regression test.

### 13 — Tool Calling + API Agents
**Scenario:** synthetic enterprise service-management agent.  
**BUILD:** schemas, registry, validation, RBAC, risk classes, approval, idempotency.  
**TRY:** retries/timeouts + tool-result validation.  
**BREAK:** malformed args, malicious output, unauthorized tool, duplicate mutation.  
**MEASURE:** tool success, denial rate, duplicate-effect rate, latency, cost.  
**DEFEND:** tool output is untrusted data.  
**Gold:** exact-action approval binding.

### 14 — Raw Agent Loop
**Scenario:** framework-free incident triage.  
**BUILD:** OBSERVE→DECIDE→ACT→VERIFY→RECOVER/STOP.  
**TRY:** hard step/token/tool budgets + repeated-state detection.  
**BREAK:** infinite loop, oscillation, false verification, duplicate action, stale observation.  
**MEASURE:** success, steps/task, recovery, loop amplification, cost.  
**DEFEND:** model-controlled vs deterministic boundaries.  
**Gold:** replayable trajectory capture.

### 15 — Memory
**Scenario:** tenant-scoped enterprise support memory.  
**BUILD:** working, episodic, semantic, procedural, user and task memory.  
**TRY:** provenance, confidence, importance, contradiction, supersession.  
**BREAK:** poisoned memory, stale preference, tenant leakage, permission drift.  
**MEASURE:** retrieval usefulness, contradiction rate, stale rate, storage growth.  
**DEFEND:** persistence changes the threat model.  
**Gold:** gated memory promotion + forgetting.

### 16 — LangGraph Stateful Workflows
**Scenario:** recoverable approval workflow.  
**BUILD:** typed state, nodes, routers, checkpoints.  
**TRY:** conditional edges, reducers, interrupts, parallel branches.  
**BREAK:** stale state, duplicate branch, cancellation, deadline, replay divergence.  
**MEASURE:** completion, recovery, transition validity, latency.  
**DEFEND:** abstraction vs state-machine mechanics.  
**Gold:** replay and locate first divergent state.

### 17 — Planning + Human-in-the-Loop
**Scenario:** synthetic procurement approvals.  
**BUILD:** planner/executor/verifier with pre/postconditions.  
**TRY:** adaptive replanning + risk-aware approval.  
**BREAK:** cyclic plan, stale approval, partial completion, mismatched high-risk action.  
**MEASURE:** plan validity, completion, escalation, time, cost.  
**DEFEND:** approval must bind to the exact action.  
**Gold:** independent plan verifier.

### 18 — Agent Security
**Scenario:** synthetic SOC investigation agent.  
**BUILD:** trust labels, policy engine, authorization, approval, egress control, audit.  
**TRY:** direct/indirect injection + tool poisoning.  
**BREAK:** confused deputy, SSRF-style request, secret leakage, cross-tenant access, replay.  
**MEASURE:** attack success, policy coverage, false-positive rate, audit completeness.  
**DEFEND:** security invariants model output cannot override.  
**Gold:** threat model + control map.

### 19 — Multi-Agent Reality Check
**Scenario:** single analyst vs specialist workers.  
**BUILD:** strong single-agent baseline.  
**TRY:** compare measured multi-agent gain.  
**BREAK:** correlated failures and coordination overhead.  
**MEASURE:** success gain, cost/success, p95 latency, disagreement.  
**DEFEND:** reject multi-agent when gain is insufficient.  
**Gold:** evidence-backed architecture decision.

### 20 — Multi-Agent Architectures
**Scenario:** supervisor/worker enterprise research.  
**BUILD:** typed task envelopes, worker registry, fan-out/fan-in.  
**TRY:** deadlines, idempotency and partial failure.  
**BREAK:** duplicate delivery, expired task, capability escalation, invalid result.  
**MEASURE:** utilization, partial success, coordination latency, duplicate effects.  
**DEFEND:** contract enforcement at delegation boundaries.  
**Gold:** supervisor cannot grant capabilities it does not possess.

### 21 — Coordination + Fault Tolerance
**Scenario:** distributed agent network.  
**BUILD:** message envelope, lease, heartbeat, retry taxonomy.  
**TRY:** backpressure, dead-letter, recovery.  
**BREAK:** stale worker, lost heartbeat, duplicate/out-of-order message, partition.  
**MEASURE:** recovery time, duplicate rate, queue depth, retry amplification.  
**DEFEND:** transient vs permanent vs authorization vs timeout failure.  
**Gold:** chaos recovery without duplicate effects.

### 22 — Multi-Agent Debugging
**Scenario:** distributed agent incident trace.  
**BUILD:** causal trace across supervisor/workers/messages/RAG/tools/verifier.  
**TRY:** first-failure detection + replay.  
**BREAK:** race, aggregation error, retrieval poisoning, policy denial.  
**MEASURE:** first-failure accuracy, causal-chain completeness, cost attribution.  
**DEFEND:** causality over event order.  
**Gold:** differential trajectory debugging.

### 23 — MCP Fundamentals
**Scenario:** synthetic enterprise capability client.  
**BUILD:** host/client/server, discovery, typed calls.  
**TRY:** resources/prompts, tenant binding, trust labels.  
**BREAK:** unauthorized capability, malicious result, schema mismatch.  
**MEASURE:** discovery correctness, denial rate, latency.  
**DEFEND:** MCP is a capability/context interface, not an authorization system.  
**Gold:** client-side trust boundary design.

### 24 — Enterprise MCP Server
**Scenario:** governed enterprise capability gateway.  
**BUILD:** authentication, authorization, catalog, audit.  
**TRY:** canonical action hashes + high-risk mutation controls.  
**BREAK:** missing idempotency, cross-role access, replay, malicious parameters.  
**MEASURE:** auth coverage, duplicate mutation rate, audit completeness.  
**DEFEND:** action identity + replay protection.  
**Gold:** fail-closed MCP gateway.

### 25 — Observability
**Scenario:** AegisAI telemetry control plane.  
**BUILD:** traces, spans, events, metrics across model/RAG/tool/MCP.  
**TRY:** critical-path + cost attribution.  
**BREAK:** missing parent span, clock skew, dropped security event, retry storm, tenant leak.  
**MEASURE:** telemetry coverage, trace completeness, p95 latency, attribution accuracy.  
**DEFEND:** connect quality with operational telemetry.  
**Gold:** incident dashboard specification.

### 26 — Production Evaluation
**Scenario:** enterprise-agent release certification.  
**BUILD:** golden cases + multidimensional gate.  
**TRY:** A/B, shadow, confidence intervals, slices.  
**BREAK:** cherry-picking, tiny samples, judge bias, safety/cost regression.  
**MEASURE:** success, safety, groundedness, latency, cost/success.  
**DEFEND:** BLOCK/WARN/PASS criteria.  
**Gold:** certify or block a release with evidence.

### 27 — Cost Engineering
**Scenario:** cost-aware enterprise router.  
**BUILD:** model, embedding, rerank, tool, storage, compute and human-review ledger.  
**TRY:** cascades, budgets, caching.  
**BREAK:** retry amplification, loop explosion, unauthorized cheap provider.  
**MEASURE:** cost/request, cost/success, quality-adjusted cost, budget utilization.  
**DEFEND:** optimize quality/latency/security jointly.  
**Gold:** cost-quality frontier.

### 28 — Responsible AI + Governance
**Scenario:** synthetic regulated workflow.  
**BUILD:** risk/data classification, eligibility, oversight, audit.  
**TRY:** policy precedence + remediation.  
**BREAK:** bypassed approval, forbidden data class, policy conflict.  
**MEASURE:** policy coverage, approval compliance, audit completeness, remediation time.  
**DEFEND:** distinguish educational controls from legal advice.  
**Gold:** turn a policy requirement into executable controls.

### 29 — Deployment + CI/CD
**Scenario:** AegisAI production release.  
**BUILD:** immutable artifact + release manifest.  
**TRY:** model/prompt/RAG/tool/policy gates, shadow, canary.  
**BREAK:** missing manifest field, failed eval gate, rollback mismatch.  
**MEASURE:** lead time, change failure rate, rollback time, gate accuracy.  
**DEFEND:** AI release identity extends beyond code.  
**Gold:** reversible release design.

### 30 — Enterprise Agentic RAG Capstone
**Scenario:** integrated synthetic enterprise Agentic RAG.  
**BUILD:** API → policy/security/budget → agent → RAG/memory/tools/MCP → verification → telemetry/evaluation → durable controls.  
**TRY:** HITL + crash recovery + release controls.  
**BREAK:** retrieval miss, tool failure, policy denial, worker crash, budget exhaustion.  
**MEASURE:** success, groundedness, citation correctness, safety, recovery, p95 latency, cost/success.  
**DEFEND:** architecture/evidence/trade-offs.  
**Gold:** portfolio-ready evidence pack.

### 31 — Knowledge Engineering & Graph RAG
**Scenario:** enterprise knowledge graph.  
**BUILD:** typed entities/claims/relations, provenance and bounded retrieval.  
**TRY:** multi-hop queries and vector-vs-graph comparison.  
**BREAK:** duplicate entity, bad relation direction, missing provenance, unbounded traversal, ACL leak.  
**MEASURE:** multi-hop accuracy, evidence quality, traversal work, latency, maintenance cost.  
**DEFEND:** when a graph is unnecessary.  
**Gold:** graph schema + benchmark + ADR.

### 32 — Graph Engineering & Temporal Knowledge
**Scenario:** time-aware enterprise ownership/policy graph.  
**BUILD:** ontology evolution, entity resolution, valid-time intervals, supersession.  
**TRY:** historical/current query comparisons.  
**BREAK:** overlapping validity, stale relation, collision, contradiction.  
**MEASURE:** temporal query accuracy, collision rate, stale-edge rate, graph health.  
**DEFEND:** valid-time vs transaction-time semantics.  
**Gold:** temporal migration + rollback plan.

### 33 — Agentic Knowledge Graph Construction
**Scenario:** maintained knowledge-ingestion agent.  
**BUILD:** propose→validate→approve→write with provenance.  
**TRY:** confidence thresholds and human review.  
**BREAK:** hallucinated claim, graph poisoning, duplicate entity, bad evidence.  
**MEASURE:** precision/recall of accepted claims, rejection rate, review load, rollback success.  
**DEFEND:** proposal is not truth.  
**Gold:** gated graph promotion pipeline.

### 34 — Graph + Vector Hybrid Retrieval
**Scenario:** multi-hop enterprise research.  
**BUILD:** vector-only, graph-only, hybrid, optional reranking.  
**TRY:** vary retrieval depth and evidence budgets.  
**BREAK:** graph miss, dense miss, wrong tenant, misleading path.  
**MEASURE:** Recall@K, MRR/nDCG, multi-hop accuracy, groundedness, latency, cost.  
**DEFEND:** identify cases where hybrid is worse.  
**Gold:** reproducible ablation matrix.

### 35 — Compounding Knowledge / LLM Wiki
**Scenario:** maintained internal knowledge base.  
**BUILD:** curated entities/claims/citations/change log.  
**TRY:** incremental updates, contradiction and supersession handling.  
**BREAK:** stale source, citation loss, poisoned update, duplicate knowledge.  
**MEASURE:** freshness lag, provenance coverage, contradiction rate, rollback success.  
**DEFEND:** why compounding requires curation rather than accumulation.  
**Gold:** knowledge-health report + rollback drill.

### 36 — Loop Engineering
**Scenario:** production loop engine.  
**BUILD:** explicit loop/state transitions, halting and budgets.  
**TRY:** verifier and recovery policy variants.  
**BREAK:** infinite loop, oscillation, retry storm, false success.  
**MEASURE:** steps/task, loop amplification, recovery rate, cost.  
**DEFEND:** control-plane invariants.  
**Gold:** compare loop policies under identical model decisions.

### 37 — Harness Engineering
**Scenario:** reusable AegisAI harness.  
**BUILD:** model adapter, context manager, tool gateway, policy, state, budget, verification, telemetry.  
**TRY:** provider/model swap without governance changes.  
**BREAK:** context ordering, tool validation, checkpoint restore, tenant isolation.  
**MEASURE:** harness overhead, task success, replay determinism, policy coverage.  
**DEFEND:** why harness belongs to the agent system.

### 38 — Long-Running Autonomous Agents
**Scenario:** durable enterprise worker.  
**BUILD:** goals/tasks/runs, leases, checkpoints, waiting/resume.  
**TRY:** scheduled work + approval persistence/revocation.  
**BREAK:** stale lease, crash after side effect, duplicate resume, revoked approval.  
**MEASURE:** resume success, duplicate-effect rate, lease expiry recovery, task latency.  
**DEFEND:** durable execution vs ordinary chat memory.  
**Gold:** crash/recovery state-machine test.

### 39 — Skills, Memory & Continual Harnesses
**Scenario:** evolving enterprise teammate.  
**BUILD:** candidate skill, evidence, validation, promotion, rollback; scoped memory.  
**TRY:** skill extraction from successful trajectories.  
**BREAK:** poisoned skill, permission drift, stale skill, memory contradiction.  
**MEASURE:** promotion precision, regression rate, retrieval usefulness, rollback rate.  
**DEFEND:** trust transition from candidate to executable capability.  
**Gold:** continual promotion gate.

### 40 — Environments, Verifiers & Agentic RL
**Scenario:** synthetic coding/operations environment.  
**BUILD:** task generator, environment contract, trajectory, verifier, reward.  
**TRY:** alternate reward and verifier designs.  
**BREAK:** reward hacking, verifier loophole, environment mismatch.  
**MEASURE:** verified success, reward/verifier disagreement, held-out performance, rollout cost.  
**DEFEND:** reward is not truth.  
**Gold:** design an anti-reward-hacking verifier suite.

### 41 — Recursive Self-Improving Agents
**Scenario:** bounded research/coding improvement engine.  
**BUILD:** baseline→hypothesis→candidate→experiment→verify→gate→deploy/rollback.  
**TRY:** compare improvement proposals against held-out regression sets.  
**BREAK:** evaluator gaming, benchmark contamination, recursion runaway, silent degradation.  
**MEASURE:** improvement delta, regression rate, rollback rate, evaluation cost.  
**DEFEND:** why self-modification needs independent gates.  
**Gold:** safe improvement controller with rollback.

### 42 — Computer Use & Always-On AI Teammates
**Scenario:** synthetic enterprise digital worker.  
**BUILD:** environment state, screenshot/DOM abstraction, action grounding, approvals and audit.  
**TRY:** scheduling + recovery from stale UI state.  
**BREAK:** stale screen/DOM, wrong target, secret exposure, unauthorized app action.  
**MEASURE:** action success, stale-state detection, policy denials, human-escalation rate.  
**DEFEND:** why visual grounding does not replace authorization.  
**Gold:** safe action loop with current-state verification.

### 43 — Frontier Graph-RAG Agentic Capstone
**Scenario:** integrated autonomous enterprise AegisAI platform.  
**BUILD:** knowledge graph + vector retrieval + harness + durable worker + tools/MCP + verification + evaluation + governance.  
**TRY:** add continual skills/memory and computer-use extension behind gates.  
**BREAK:** graph poisoning, tool failure, stale state, worker crash, verifier gap, budget exhaustion, policy denial.  
**MEASURE:** verified task success, groundedness, citation correctness, safety, recovery, p95 latency, cost/success and regression rate.  
**DEFEND:** full architecture, threat model, evaluation evidence and operating model.  
**Gold:** portfolio-ready frontier-system evidence pack.

## Review rule

When a module already has strong material, retain and link it. Do not rewrite good content merely for conformity. Normalize only the missing evidence, naming, security boundaries, measurements or progression needed by the authoritative standards.
