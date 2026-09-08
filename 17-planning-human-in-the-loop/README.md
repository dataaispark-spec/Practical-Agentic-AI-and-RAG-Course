# Module 17 — Planning + Human-in-the-Loop



## Mission
Turn a goal into an executable, verifiable plan while keeping humans in control when risk, uncertainty, cost, or policy requires it.

## Core architecture
```text
GOAL
 ↓
PLAN → VALIDATE PLAN → EXECUTE STEP → VERIFY
                  ↘ failure → REPLAN
                  ↘ risk    → HUMAN APPROVAL
                  ↘ success → NEXT STEP
                         ↓
                       DONE
```

Planning is not automatically better than a reactive agent. More planning creates overhead and can amplify an incorrect assumption. The engineering objective is the **minimum sufficient planning depth**.

## Learning outcomes
Build and compare:
- reactive agents;
- fixed plans;
- planner/executor agents;
- adaptive replanners;
- verifier-guided planners;
- approval-gated agents;
- partial-completion and escalation paths.

## Planning representations
A plan can be represented as:
- ordered steps;
- dependency DAG;
- state-transition graph;
- task/subtask hierarchy;
- executable workflow with guards.

For each step define:
- objective;
- inputs;
- expected output;
- tools permitted;
- preconditions;
- postconditions;
- risk class;
- timeout/budget;
- verification method;
- rollback or recovery action.

## Planner vs executor
Separate responsibilities:

**Planner:** decomposes the goal, identifies dependencies, proposes sequence and acceptance criteria.

**Executor:** performs one bounded step under policy and records evidence.

**Verifier:** independently determines whether the step or task actually succeeded.

This separation prevents the same reasoning process from both making and approving its own claims.

## Adaptive replanning
Replanning should occur when:
- a precondition becomes false;
- a tool fails permanently;
- evidence contradicts the plan;
- cost exceeds threshold;
- a new dependency appears;
- policy changes;
- human feedback changes requirements.

Do not replan merely because the model is uncertain. Define explicit triggers.

## Human-in-the-loop levels
1. **Notify** — human sees the action but does not block it.
2. **Approve** — execution waits for approval.
3. **Edit** — human modifies the proposed action/plan.
4. **Choose** — human selects among alternatives.
5. **Take over** — human assumes control.

Use risk and reversibility to determine the level.

## Approval contract
An approval request should contain:
- task ID;
- proposed action;
- exact parameters;
- expected effect;
- risk classification;
- evidence;
- alternatives;
- expiration;
- approver identity;
- audit ID.

An approval should bind to the exact action, not merely to a vague intention such as “approve the plan.”

## Lab 1 — Reactive baseline
Use Module 14's agent loop on a multi-step task. Record success, steps and tool calls.

## Lab 2 — Fixed planner/executor
Create a planner that produces a sequence and an executor that performs each step.

**Exercise:** Add preconditions and postconditions.

## Lab 3 — DAG planning
Represent dependencies as a DAG and execute independent steps safely.

**Failure injection:** introduce a dependency cycle and prove the planner rejects it.

## Lab 4 — Replanning
Make step 2 fail because a precondition changed. Generate a new plan from the current state rather than restarting from scratch.

## Lab 5 — Verification-guided planning
Give the executor a plausible but incorrect result. Require independent verification before progressing.

## Lab 6 — Human approval
Add approval before a high-impact action. Test approve, reject, edit, timeout and expired approval.

## Lab 7 — Partial completion
Force failure halfway through a five-step plan. Resume from the last verified checkpoint without repeating safe completed work.

## Lab 8 — Plan quality benchmark
Compare reactive, fixed-plan and adaptive-plan agents on the same benchmark.

Measure success, planning latency, execution latency, tool calls, replans, cost and unsafe attempts.

## Lab 9 — Cost-aware planning
Give actions different token/tool/time costs. Select a plan under a hard budget.

## Lab 10 — Adversarial planning
Inject malicious observations that attempt to change the goal or bypass approval. Prove policy remains authoritative.

## Detailed exercises
1. Define a task contract.
2. Build a plan schema.
3. Add preconditions.
4. Add postconditions.
5. Add dependency validation.
6. Detect cycles.
7. Implement plan execution.
8. Add step verification.
9. Add replan triggers.
10. Add plan versioning.
11. Add approval requests.
12. Bind approvals to exact actions.
13. Implement approval expiry.
14. Implement rejection paths.
15. Implement human edits.
16. Implement escalation.
17. Implement checkpoint resume.
18. Implement partial completion.
19. Add cost-aware plan selection.
20. Build planner/executor regression tests.

## Failure-first scenarios
### Goal drift
An observation attempts to replace the original objective. Reject unauthorized goal mutation.

### Plan hallucination
Planner references a nonexistent tool or capability. Validate before execution.

### Dependency failure
A downstream step executes despite a failed prerequisite. Enforce preconditions.

### Approval mismatch
Approved action differs from the action eventually executed. Treat the approval as invalid.

### Approval replay
An old approval is reused for a new action. Bind approval to action hash + task state/version.

### Replanning storm
Every small observation triggers a new plan. Add explicit replanning thresholds and budgets.

### False verification
Verifier accepts an unsupported claim. Require evidence and independent checks.

### Partial failure
Step 4 fails after steps 1–3 succeeded. Resume from verified state and avoid duplicate side effects.

## Production metrics
Track:
- task success rate;
- plan validity rate;
- plan execution success;
- replans/task;
- approval rate;
- approval latency;
- rejection rate;
- verification failure rate;
- unsafe-action attempts;
- steps/task;
- tool calls/task;
- cost/task;
- p50/p95 completion time.

## Production architecture
```text
              Goal
               ↓
        Planner / Replanner
               ↓
          Plan Validator
               ↓
       Policy + Risk Engine
          ↙           ↘
     Execute        Approval
        ↓              ↓
      Verify ←──── Human
        ↓
  Checkpoint / State
        ↓
   Continue / Replan / Escalate / Stop
```

## Industry scenarios
**Banking:** investigate a suspicious transaction, gather evidence, prepare a recommendation, and require approval before any customer/account action.

**Cybersecurity:** triage an incident, collect non-destructive evidence automatically, then request approval before containment.

**Enterprise IT:** diagnose an outage using approved diagnostics, propose remediation, obtain approval for production changes, execute and verify.

**Procurement:** compare suppliers and prepare a purchase recommendation, but require explicit approval before creating a binding order.

## Interview questions
1. When is planning worse than a reactive loop?
2. Planner vs executor responsibilities?
3. Why use a separate verifier?
4. What should trigger replanning?
5. How do you prevent replanning storms?
6. What is a plan DAG?
7. How do you handle partial completion?
8. How should approvals be bound?
9. Why can “approve this plan” be unsafe?
10. How do you expire approvals?
11. How do you defend against goal drift?
12. How do you benchmark planning quality?
13. How do you make planning cost-aware?
14. What happens when a plan references an unavailable tool?
15. How would you resume after a process crash?

## System-design challenge
Design a planning service for 50,000 concurrent agent tasks with DAG validation, durable checkpoints, adaptive replanning, independent verification, risk-based human approval, auditability and strict cost/time budgets.

## Mastery gate
Build an adaptive planner that completes a multi-step task, verifies every critical transition, survives a mid-plan failure, replans when state changes, and requires exact-action approval for high-impact operations.

## Gold challenge
Benchmark reactive, fixed-plan, planner/executor and adaptive verifier-guided agents across at least 100 tasks. Report success, cost, latency, replans, tool calls, verification failures and unsafe-action attempts. Select the architecture using evidence rather than intuition.

## Google Colab
`notebooks/module_17_planning_human_in_the_loop.ipynb` is a self-contained executable lab covering plan creation, DAG validation, execution, verification, replanning, approval gates, partial recovery and benchmarking.

## Expanded long-form course chapter

This course is a practical engineering progression from deterministic software and LLM applications to retrieval, tools, stateful agents, distributed coordination, knowledge graphs, durable autonomy, verification, computer use, and controlled self-improvement. The governing idea is that an AI system becomes production-grade not by adding more model calls, but by adding explicit boundaries around probabilistic decisions. Throughout the 43 modules, the learner repeatedly asks: What is the goal? What state is authoritative? What evidence is available? What actions are permitted? What budget applies? What must be verified? What happens when a dependency fails? What must be observable and auditable? What evidence would justify changing the design?

The course uses the AegisAI mental model: Model + Harness + Environment + Tools + State + Policy + Budget + Verification. Retrieval is treated as a knowledge mechanism; an agent loop is treated as a decision-and-action mechanism; a harness is treated as the control plane around the model; and a verifier is treated as an independent check on outcomes. This distinction prevents a common engineering failure in which a prompt is asked to perform authorization, correctness checking, persistence, and business policy simultaneously.

Every module follows the same learning rhythm: Predict → Run → Observe → Explain → Break → Debug → Measure → Improve → Defend. The examples therefore emphasize observable mechanisms, explicit contracts, failure injection, metrics, and regression tests. The notebooks and applications are intended to work with deterministic fakes and synthetic data wherever possible, so that the learner can understand the mechanism before depending on a commercial provider.

## Module-specific learning contract

This expanded chapter deepens the repository canonical learning objectives for **Module 17: Planning + Human-in-the-Loop**. The objective vocabulary is preserved: planning, planner executor, preconditions, postconditions, human approval, and replanning. Each concept is connected to architecture, implementation, failure analysis, evaluation, security, operations and system-design reasoning.

## First-principles concepts

### 1. Planning

The first principle for Planning + Human-in-the-Loop is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, planning should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Planner Executor

A practical way to learn Planning + Human-in-the-Loop is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for planner executor; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Preconditions

In an enterprise setting, Planning + Human-in-the-Loop rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. preconditions becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Postconditions

The failure-first perspective is especially important for Planning + Human-in-the-Loop. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For postconditions, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Human Approval

Measurement should accompany every meaningful change to Planning + Human-in-the-Loop. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For human approval, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Replanning

A useful architecture diagram for Planning + Human-in-the-Loop separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For replanning, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Planning

Versioning is part of the technical design of Planning + Human-in-the-Loop, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If planning changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Planner Executor

The final production question for Planning + Human-in-the-Loop is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For planner executor, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Architecture and control boundaries

### 1. Planning

The first principle for Planning + Human-in-the-Loop is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, planning should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Planner Executor

A practical way to learn Planning + Human-in-the-Loop is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for planner executor; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Preconditions

In an enterprise setting, Planning + Human-in-the-Loop rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. preconditions becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Postconditions

The failure-first perspective is especially important for Planning + Human-in-the-Loop. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For postconditions, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Human Approval

Measurement should accompany every meaningful change to Planning + Human-in-the-Loop. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For human approval, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Replanning

A useful architecture diagram for Planning + Human-in-the-Loop separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For replanning, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Planning

Versioning is part of the technical design of Planning + Human-in-the-Loop, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If planning changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Planner Executor

The final production question for Planning + Human-in-the-Loop is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For planner executor, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Mechanisms and implementation reasoning

### 1. Planning

The first principle for Planning + Human-in-the-Loop is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, planning should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Planner Executor

A practical way to learn Planning + Human-in-the-Loop is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for planner executor; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Preconditions

In an enterprise setting, Planning + Human-in-the-Loop rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. preconditions becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Postconditions

The failure-first perspective is especially important for Planning + Human-in-the-Loop. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For postconditions, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Human Approval

Measurement should accompany every meaningful change to Planning + Human-in-the-Loop. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For human approval, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Replanning

A useful architecture diagram for Planning + Human-in-the-Loop separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For replanning, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Planning

Versioning is part of the technical design of Planning + Human-in-the-Loop, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If planning changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Planner Executor

The final production question for Planning + Human-in-the-Loop is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For planner executor, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Industry scenarios and worked examples

### 1. Planning

The first principle for Planning + Human-in-the-Loop is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, planning should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Planner Executor

A practical way to learn Planning + Human-in-the-Loop is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for planner executor; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Preconditions

In an enterprise setting, Planning + Human-in-the-Loop rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. preconditions becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Postconditions

The failure-first perspective is especially important for Planning + Human-in-the-Loop. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For postconditions, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Human Approval

Measurement should accompany every meaningful change to Planning + Human-in-the-Loop. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For human approval, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Replanning

A useful architecture diagram for Planning + Human-in-the-Loop separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For replanning, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Planning

Versioning is part of the technical design of Planning + Human-in-the-Loop, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If planning changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Planner Executor

The final production question for Planning + Human-in-the-Loop is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For planner executor, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Failure-first engineering

### 1. Planning

The first principle for Planning + Human-in-the-Loop is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, planning should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Planner Executor

A practical way to learn Planning + Human-in-the-Loop is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for planner executor; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Preconditions

In an enterprise setting, Planning + Human-in-the-Loop rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. preconditions becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Postconditions

The failure-first perspective is especially important for Planning + Human-in-the-Loop. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For postconditions, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Human Approval

Measurement should accompany every meaningful change to Planning + Human-in-the-Loop. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For human approval, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Replanning

A useful architecture diagram for Planning + Human-in-the-Loop separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For replanning, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Planning

Versioning is part of the technical design of Planning + Human-in-the-Loop, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If planning changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Planner Executor

The final production question for Planning + Human-in-the-Loop is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For planner executor, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Experiments and measurement

### 1. Planning

The first principle for Planning + Human-in-the-Loop is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, planning should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Planner Executor

A practical way to learn Planning + Human-in-the-Loop is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for planner executor; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Preconditions

In an enterprise setting, Planning + Human-in-the-Loop rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. preconditions becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Postconditions

The failure-first perspective is especially important for Planning + Human-in-the-Loop. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For postconditions, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Human Approval

Measurement should accompany every meaningful change to Planning + Human-in-the-Loop. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For human approval, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Replanning

A useful architecture diagram for Planning + Human-in-the-Loop separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For replanning, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Planning

Versioning is part of the technical design of Planning + Human-in-the-Loop, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If planning changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Planner Executor

The final production question for Planning + Human-in-the-Loop is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For planner executor, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Security, governance and responsible operation

### 1. Planning

The first principle for Planning + Human-in-the-Loop is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, planning should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Planner Executor

A practical way to learn Planning + Human-in-the-Loop is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for planner executor; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Preconditions

In an enterprise setting, Planning + Human-in-the-Loop rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. preconditions becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Postconditions

The failure-first perspective is especially important for Planning + Human-in-the-Loop. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For postconditions, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Human Approval

Measurement should accompany every meaningful change to Planning + Human-in-the-Loop. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For human approval, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Replanning

A useful architecture diagram for Planning + Human-in-the-Loop separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For replanning, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Planning

Versioning is part of the technical design of Planning + Human-in-the-Loop, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If planning changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Planner Executor

The final production question for Planning + Human-in-the-Loop is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For planner executor, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Production design and operational readiness

### 1. Planning

The first principle for Planning + Human-in-the-Loop is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, planning should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Planner Executor

A practical way to learn Planning + Human-in-the-Loop is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for planner executor; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Preconditions

In an enterprise setting, Planning + Human-in-the-Loop rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. preconditions becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Postconditions

The failure-first perspective is especially important for Planning + Human-in-the-Loop. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For postconditions, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Human Approval

Measurement should accompany every meaningful change to Planning + Human-in-the-Loop. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For human approval, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Replanning

A useful architecture diagram for Planning + Human-in-the-Loop separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For replanning, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Planning

Versioning is part of the technical design of Planning + Human-in-the-Loop, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If planning changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Planner Executor

The final production question for Planning + Human-in-the-Loop is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For planner executor, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Debugging and incident analysis

### 1. Planning

The first principle for Planning + Human-in-the-Loop is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, planning should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Planner Executor

A practical way to learn Planning + Human-in-the-Loop is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for planner executor; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Preconditions

In an enterprise setting, Planning + Human-in-the-Loop rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. preconditions becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Postconditions

The failure-first perspective is especially important for Planning + Human-in-the-Loop. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For postconditions, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Human Approval

Measurement should accompany every meaningful change to Planning + Human-in-the-Loop. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For human approval, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Replanning

A useful architecture diagram for Planning + Human-in-the-Loop separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For replanning, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Planning

Versioning is part of the technical design of Planning + Human-in-the-Loop, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If planning changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Planner Executor

The final production question for Planning + Human-in-the-Loop is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For planner executor, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Exercises and independent practice

### 1. Planning

The first principle for Planning + Human-in-the-Loop is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, planning should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Planner Executor

A practical way to learn Planning + Human-in-the-Loop is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for planner executor; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Preconditions

In an enterprise setting, Planning + Human-in-the-Loop rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. preconditions becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Postconditions

The failure-first perspective is especially important for Planning + Human-in-the-Loop. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For postconditions, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Human Approval

Measurement should accompany every meaningful change to Planning + Human-in-the-Loop. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For human approval, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Replanning

A useful architecture diagram for Planning + Human-in-the-Loop separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For replanning, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Planning

Versioning is part of the technical design of Planning + Human-in-the-Loop, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If planning changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Planner Executor

The final production question for Planning + Human-in-the-Loop is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For planner executor, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## System-design review

### 1. Planning

The first principle for Planning + Human-in-the-Loop is to make the boundary explicit. A production implementation should state what enters the component, what leaves it, what state it may mutate, what policy constrains it, and what evidence proves that the operation succeeded. When those boundaries are hidden inside a framework, failures become difficult to localize. In this module, planning should therefore be treated as an engineering contract rather than a collection of API calls. A useful review asks which decisions are deterministic, which decisions are probabilistic, which data is trusted, and which observations are required to reconstruct a failed run.

### 2. Planner Executor

A practical way to learn Planning + Human-in-the-Loop is to start with the smallest executable mechanism and then add one production constraint at a time. Begin with a happy-path example for planner executor; add typed inputs; introduce malformed input; introduce a dependency timeout; add a policy restriction; add telemetry; then replay the same scenario. This progression makes cause and effect visible. Do not add architecture merely because the technology is available. Add it when a measured requirement or failure mode justifies the complexity.

### 3. Preconditions

In an enterprise setting, Planning + Human-in-the-Loop rarely exists in isolation. Identity, tenancy, data classification, latency objectives, cost limits, audit requirements and operational ownership all change the design. A mechanism that works for a personal prototype may be unacceptable when the same request can cross a tenant boundary or trigger a financial action. The correct design combines the technical mechanism with deterministic controls outside the model. preconditions becomes useful only when the surrounding system can enforce who may use it, what evidence it may access, what it may change, and how the result will be checked.

### 4. Postconditions

The failure-first perspective is especially important for Planning + Human-in-the-Loop. A system that works on the happy path proves very little. The stronger question is what happens when input is incomplete, a dependency is slow, returned data is contradictory, a user disconnects, policy changes, state is stale, or an attacker deliberately supplies hostile content. For postconditions, define the expected observable before injecting the fault. Record the first failing stage, containment boundary, recovery action, and regression assertion. This converts debugging from intuition into an experiment.

### 5. Human Approval

Measurement should accompany every meaningful change to Planning + Human-in-the-Loop. Quality, latency and cost are often coupled. Larger context may improve answer quality but increase latency and token cost. More retries may improve availability during short outages while amplifying load during a large outage. A stronger verifier may reduce unsafe actions while increasing response time. For human approval, maintain a scorecard containing task success, relevant quality metrics, p50/p95 latency, resource consumption, failure rate, and policy or verification failures. The goal is to make trade-offs explicit.

### 6. Replanning

A useful architecture diagram for Planning + Human-in-the-Loop separates mechanism from control. The mechanism performs useful work; the control plane establishes identity, validates inputs, enforces authorization, manages budgets, records telemetry, and verifies outcomes. For replanning, draw both layers. Ask whether the system would remain safe if the model produced a wrong answer. If not, a critical control is probably living in the wrong place. Production AI engineering moves irreversible decisions away from untrusted model output and toward deterministic policy, typed interfaces and independent verification.

### 7. Planning

Versioning is part of the technical design of Planning + Human-in-the-Loop, not an administrative afterthought. Prompts, models, embeddings, retrieval indexes, policies, tools, graph schemas, memory records and verifier rules can all change behavior. If planning changes without a version identifier, a later incident may be impossible to reproduce. A practical implementation records the versions involved in each important run and defines a rollback boundary. The learner should be able to answer not only what the system did, but which artifact versions caused it to behave that way.

### 8. Planner Executor

The final production question for Planning + Human-in-the-Loop is whether the mechanism improves the business outcome enough to justify its operational cost. A technically elegant system can still be a poor product if it is too slow, too expensive, too difficult to monitor, or too risky. For planner executor, compare the mechanism with a simpler baseline. State the baseline, measurable improvement, new failure modes, and operational burden. Use the simplest architecture that meets the requirement, and add complexity only when evidence shows that the additional capability creates value.

## Assessment and mastery

### Question 1

Explain how you would design, implement, test, observe and defend **planning** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 2

Explain how you would design, implement, test, observe and defend **planner executor** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 3

Explain how you would design, implement, test, observe and defend **preconditions** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 4

Explain how you would design, implement, test, observe and defend **postconditions** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 5

Explain how you would design, implement, test, observe and defend **human approval** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 6

Explain how you would design, implement, test, observe and defend **replanning** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 7

Explain how you would design, implement, test, observe and defend **planning** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 8

Explain how you would design, implement, test, observe and defend **planner executor** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 9

Explain how you would design, implement, test, observe and defend **preconditions** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 10

Explain how you would design, implement, test, observe and defend **postconditions** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 11

Explain how you would design, implement, test, observe and defend **human approval** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 12

Explain how you would design, implement, test, observe and defend **replanning** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 13

Explain how you would design, implement, test, observe and defend **planning** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 14

Explain how you would design, implement, test, observe and defend **planner executor** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 15

Explain how you would design, implement, test, observe and defend **preconditions** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 16

Explain how you would design, implement, test, observe and defend **postconditions** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 17

Explain how you would design, implement, test, observe and defend **human approval** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 18

Explain how you would design, implement, test, observe and defend **replanning** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 19

Explain how you would design, implement, test, observe and defend **planning** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 20

Explain how you would design, implement, test, observe and defend **planner executor** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 21

Explain how you would design, implement, test, observe and defend **preconditions** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 22

Explain how you would design, implement, test, observe and defend **postconditions** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 23

Explain how you would design, implement, test, observe and defend **human approval** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 24

Explain how you would design, implement, test, observe and defend **replanning** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 25

Explain how you would design, implement, test, observe and defend **planning** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 26

Explain how you would design, implement, test, observe and defend **planner executor** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 27

Explain how you would design, implement, test, observe and defend **preconditions** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 28

Explain how you would design, implement, test, observe and defend **postconditions** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 29

Explain how you would design, implement, test, observe and defend **human approval** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

### Question 30

Explain how you would design, implement, test, observe and defend **replanning** in a real Planning + Human-in-the-Loop system. Include one happy path, one failure path, one security concern, one measurable metric and one regression test.

## Mastery gate

Completion means being able to explain the mechanism from first principles, implement the smallest working version, deliberately break it, identify the first failing boundary from evidence, repair it, measure the repaired system against a baseline, and defend the resulting trade-offs. The learner should also explain when not to use the mechanism. Production expertise includes recognizing when a simpler deterministic solution is safer, cheaper and easier to operate.

## Deep case study 1: Planning

Consider an enterprise workload in which planning is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why planning cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 2: Planner Executor

Consider an enterprise workload in which planner executor is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why planner executor cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 3: Preconditions

Consider an enterprise workload in which preconditions is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why preconditions cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 4: Postconditions

Consider an enterprise workload in which postconditions is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why postconditions cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 5: Human Approval

Consider an enterprise workload in which human approval is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why human approval cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 6: Replanning

Consider an enterprise workload in which replanning is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why replanning cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 7: Planning

Consider an enterprise workload in which planning is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why planning cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 8: Planner Executor

Consider an enterprise workload in which planner executor is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why planner executor cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 9: Preconditions

Consider an enterprise workload in which preconditions is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why preconditions cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 10: Postconditions

Consider an enterprise workload in which postconditions is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why postconditions cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 11: Human Approval

Consider an enterprise workload in which human approval is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why human approval cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 12: Replanning

Consider an enterprise workload in which replanning is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why replanning cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 13: Planning

Consider an enterprise workload in which planning is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why planning cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 14: Planner Executor

Consider an enterprise workload in which planner executor is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why planner executor cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 15: Preconditions

Consider an enterprise workload in which preconditions is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why preconditions cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 16: Postconditions

Consider an enterprise workload in which postconditions is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why postconditions cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 17: Human Approval

Consider an enterprise workload in which human approval is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why human approval cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 18: Replanning

Consider an enterprise workload in which replanning is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why replanning cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 19: Planning

Consider an enterprise workload in which planning is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why planning cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 20: Planner Executor

Consider an enterprise workload in which planner executor is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why planner executor cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 21: Preconditions

Consider an enterprise workload in which preconditions is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why preconditions cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 22: Postconditions

Consider an enterprise workload in which postconditions is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why postconditions cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 23: Human Approval

Consider an enterprise workload in which human approval is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why human approval cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 24: Replanning

Consider an enterprise workload in which replanning is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why replanning cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 25: Planning

Consider an enterprise workload in which planning is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why planning cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 26: Planner Executor

Consider an enterprise workload in which planner executor is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why planner executor cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 27: Preconditions

Consider an enterprise workload in which preconditions is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why preconditions cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 28: Postconditions

Consider an enterprise workload in which postconditions is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why postconditions cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 29: Human Approval

Consider an enterprise workload in which human approval is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why human approval cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 30: Replanning

Consider an enterprise workload in which replanning is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why replanning cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 31: Planning

Consider an enterprise workload in which planning is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why planning cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 32: Planner Executor

Consider an enterprise workload in which planner executor is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why planner executor cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.

## Deep case study 33: Preconditions

Consider an enterprise workload in which preconditions is a material part of the decision path. Start by stating the business outcome, users, data boundary, expected action, and failure cost. Establish a baseline before introducing the module mechanism. Then define the smallest implementation that demonstrates it. Instrument the boundary so a reviewer can see inputs, intermediate state, decisions, outputs, latency and resource usage without exposing secrets or unnecessary personal data. Introduce one controlled failure at a time: malformed input, missing evidence, stale state, dependency timeout, authorization mismatch, contradictory data, unexpected model output, or policy change. For each failure, identify the first observable deviation from the expected contract. Do not jump directly to a fix; write a hypothesis and run an experiment that distinguishes it from competing explanations. After the fix, replay the same failure and verify that the regression test protects the boundary. Finally, compare the improved implementation with the baseline on task success, latency, cost and operational complexity. A strong design review should explain why the architecture is sufficient, which alternatives were rejected, what evidence supports the decision, and what future observation would justify revisiting it.

This case also illustrates why preconditions cannot be delegated blindly to a language model. If the model produces an incorrect recommendation, the surrounding application must still enforce authorization, budget, data access, and verification. Where an action is irreversible or high impact, introduce an approval boundary or deterministic verifier. Where information is uncertain, represent uncertainty rather than manufacturing confidence. Where knowledge can become stale, record versions and effective dates. Where the workload is multi-tenant, apply tenant isolation before candidate truncation or action selection. Where the system is long-running, persist state and make side effects idempotent. These controls are the engineering environment in which the module mechanism becomes trustworthy.
