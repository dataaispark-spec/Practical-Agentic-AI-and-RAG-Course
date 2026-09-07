# Module 17 — Planning, Replanning & Human-in-the-Loop

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
