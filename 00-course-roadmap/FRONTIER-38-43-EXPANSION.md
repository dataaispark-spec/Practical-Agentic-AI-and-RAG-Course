# Frontier Modules 38–43 — World-Class Expansion Specification

This specification raises Modules 38–43 to the same theory-first, failure-first, measurement-driven standard established in Modules 35–37. The progression is deliberate:

**38 Durable → 39 Learn/Remember → 40 Environment/Verify → 41 Improve → 42 Act in the UI world → 43 Integrate everything.**

## Common module contract
Every module must teach: problem → mental model → architecture → component internals → invariants → implementation → BUILD → TRY → BREAK → DEBUG → MEASURE → IMPROVE → DEFEND → domain lab → coding challenge → debugging challenge → system design → production ADR → mastery gate.

Every notebook follows `Predict → Build → Try → Break → Debug → Measure → Improve → Defend` and must run without paid API credentials using deterministic fixtures. Production integrations are extension exercises, never prerequisites.

---

## 38 — Long-Running Autonomous Agents

### Core theory
Teach the difference between a short-lived agent run and durable execution. Cover goal/task/run/attempt identity, state machines, leases, heartbeats, fencing tokens, checkpoint semantics, event sourcing, wake/sleep, timers, webhooks, approvals, deadlines, cumulative budgets, retries, backpressure, dead-letter queues, reconciliation and exactly-once-vs-at-least-once realities.

### Architecture
```text
EVENT/SCHEDULE → DURABLE TASK → QUEUE → LEASE/FENCE → WORKER
                                      ↓          ↓
                                  CHECKPOINT   EFFECT
                                      ↓          ↓
                             WAIT/RECOVER ← VERIFY
                                      ↓
                              RESUME/STOP/ESCALATE
```

### Domain labs
Banking reconciliation; SOC investigations; database migrations; overnight research; enterprise ticket remediation; supply-chain exception processing.

### Failure labs
Crash before effect, timeout after effect, duplicate delivery, split brain, expired approval, stale policy, zombie worker, provider outage, poisoned checkpoint, runaway wakeups, budget exhaustion.

### Required evidence
Recovery matrix, idempotency proof, lease/fencing test, checkpoint benchmark, recovery-time measurement, cost/run analysis and incident reconstruction.

---

## 39 — Skills, Memory & Continual Harnesses

### Core theory
Separate episodic memory, semantic memory, procedural skill and policy. Teach memory lifecycle, salience, provenance, confidence, temporal validity, tenant scope, retrieval, contradiction, expiry, forgetting, skill versioning, candidate/trusted/rejected/deprecated states and regression-gated promotion.

### Architecture
```text
TRAJECTORY → EXPERIENCE → CANDIDATE MEMORY/SKILL
                         ↓
              PROVENANCE + VALIDATION
                         ↓
                 REGRESSION SUITE
                         ↓
              PROMOTION / REJECT / EXPIRE
                         ↓
              TRUSTED REGISTRY → HARNESS
                         ↘ ROLLBACK
```

### Domain labs
SOC playbook learning; customer-support procedures; SRE runbooks; enterprise sales knowledge; clinical/regulated workflow simulation using synthetic data.

### Failure labs
Memory poisoning, stale skill, contradictory memory, cross-tenant retrieval, privilege drift, unsafe procedural promotion, regression after reuse, silent deletion and provenance loss.

### Required evidence
Memory/skill taxonomy, promotion policy, regression suite, rollback demonstration, poisoning test, retrieval-quality and reuse-cost benchmark.

---

## 40 — Environments, Verifiers & Agentic RL

### Core theory
Define an environment as the measurable world, not merely a prompt. Teach reset/seed semantics, observation/action spaces, trajectory identity, deterministic verifiers, semantic/model-assisted verifiers, reward design, reward misspecification, reward hacking, judge bias, verifier independence, offline evaluation, held-out tasks, adversarial evaluation and safe policy improvement.

### Architecture
```text
TASK → ENVIRONMENT → POLICY/AGENT → TRAJECTORY
                         ↓              ↓
                    ACTIONS        ARTIFACTS
                         ↓              ↓
                       STATE → VERIFIER → SCORE
                                      ↓
                              EVALUATION/REPLAY
                                      ↓
                                IMPROVEMENT
```

### Domain labs
Coding sandbox; SOC remediation simulator; database migration simulator; procurement workflow; support-ticket resolution.

### Failure labs
Simulator shortcut, reward hacking, evaluator capture, test deletion, artifact tampering, judge disagreement, contamination between training and evaluation, environment escape.

### Required evidence
Seeded replay, verifier confusion matrix, weak-vs-hardened reward experiment, held-out benchmark, safety constraints and sandbox isolation proof.

---

## 41 — Recursive & Self-Improving Agents

### Core theory
Teach improvement as controlled experimentation, not uncontrolled self-modification. Define improvement surfaces: prompt, retrieval, tool routing, skill, memory policy, planner, verifier and harness. Cover hypothesis generation, candidate isolation, baseline/candidate comparison, causal attribution, experiment budgets, evaluator independence, canary releases, rollback, recursion depth and authority invariants.

### Architecture
```text
PRODUCTION TRAJECTORIES → FAILURE MINING → HYPOTHESIS
                                      ↓
                                CANDIDATE
                                      ↓
                         SANDBOX + INDEPENDENT TESTS
                                      ↓
                       SECURITY + HELD-OUT EVALUATION
                                      ↓
                              CANARY / ROLLBACK
                                      ↓
                               TRUSTED RELEASE
```

### Domain labs
Prompt optimizer; retrieval optimizer; tool-selection optimizer; incident-recovery optimizer; skill-improvement pipeline.

### Failure labs
Benchmark gaming, evaluator capture, regression hiding, distribution overfitting, recursive runaway, self-granted authority, poisoned training trajectories and rollback failure.

### Required evidence
Immutable improvement ledger, fixed/adversarial/held-out scores, security regression matrix, experiment cost, canary decision and rollback proof.

---

## 42 — Computer Use & Always-On AI Teammates

### Core theory
Teach UI agents as partially observed control systems. Compare screenshot, DOM, accessibility tree and API observations; model coordinate/semantic actions, preconditions, postconditions, stale UI, focus/window state, navigation, session expiry, credential brokering, DLP, approval, scheduling and emergency shutdown.

### Architecture
```text
GOAL → POLICY/IDENTITY → OBSERVE(UI/API) → PLAN
                              ↓             ↓
                     SCREEN/DOM/A11Y   ACTION CONTRACT
                              ↓             ↓
                          ENVIRONMENT → VERIFY
                              ↓
                       DURABLE STATE/AUDIT
```

### Domain labs
CRM operations; service desk; finance operations with synthetic accounts; browser-based research; CI/CD operations; procurement workflow.

### Failure labs
Clicking stale controls, webpage prompt injection, secret exfiltration, wrong-account action, session expiry, duplicate submission, approval expiry, runaway scheduled trigger.

### Required evidence
API-first vs UI benchmark, stale-state test, credential isolation, DLP test, approval binding, postcondition verification and emergency stop.

---

## 43 — Frontier Graph-RAG Agentic Capstone

### Mission
Integrate the complete course into AegisAI while preserving architectural boundaries. The capstone is not a feature checklist: learners must demonstrate measurable value and prove that every autonomous capability remains governed.

### Reference architecture
```text
BUSINESS EVENT/USER
       ↓
TASK + RISK + TENANT + BUDGET
       ↓
POLICY / IDENTITY / APPROVAL
       ↓
HARNESS + LOOP + DURABLE EXECUTION
   ↙        ↓          ↘
GRAPHRAG  MEMORY/SKILLS  TOOLS/MCP/UI
   ↘        ↓          ↙
       ENVIRONMENT
           ↓
  INDEPENDENT VERIFIER
           ↓
   RESULT + TRACE + AUDIT
           ↓
EVALUATION → SHADOW → CANARY → ROLLBACK
           ↘ CONTROLLED IMPROVEMENT
```

### Capstone domains
SOC; SRE; banking reconciliation; enterprise research; coding teammate; procurement; customer operations.

### Progressive implementation
Baseline deterministic workflow → RAG → GraphRAG → agent loop → governed harness → durable worker → memory/skills → verifier environment → computer use → controlled improvement.

### Chaos scenarios
Retrieval miss, stale graph edge, tenant leakage, malformed tool call, provider outage, duplicate mutation, false verification, checkpoint corruption, approval expiry, poisoned memory, poisoned skill, UI injection, reward hacking and self-improvement regression.

### Final scorecard
Retrieval Recall@K/MRR; multi-hop accuracy; citation correctness; groundedness; task success; verifier precision/recall; unauthorized-action rate; recovery success; resume success; p95 latency; cost/success; trace completeness; computer-use verified success; improvement delta; security regression rate.

### Graduation standard
The learner must defend why a simpler architecture would or would not suffice, reproduce every major failure, demonstrate recovery, quantify economics, explain governance boundaries and prove that no model, memory, graph, tool result or self-improvement candidate can silently acquire authority.

---

## Repository standard for 38–43
Each canonical module should expose:

```text
README.md
EXERCISES.md
app/
notebooks/<canonical-module-notebook>.ipynb
theory/
domain-labs/
benchmarks/
assessment/
tests/
```

`theory/` teaches mechanism and invariants; `domain-labs/` supplies realistic scenarios; `benchmarks/` makes claims measurable; `assessment/` defines mastery evidence; `app/` contains deterministic reference mechanisms; `tests/` protects correctness.

The existing Modules 38–43 notebooks already contain substantial failure-first material; this expansion makes the surrounding theory, folder contract, domain practice, benchmarks and mastery evidence equally explicit rather than leaving the depth hidden inside notebooks.
