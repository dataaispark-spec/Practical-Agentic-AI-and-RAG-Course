# Module 14 — Raw Agent Loop Engineering

## Mission
Build an agent loop from first principles so the framework abstractions used later are understandable, measurable and debuggable.

## The canonical loop
```text
OBSERVE → DECIDE → ACT → VERIFY → RECOVER / CONTINUE / STOP
```

The model proposes decisions; deterministic code owns state, budgets, policy, tool dispatch, verification and termination.

## Learning outcomes
You will build:
- explicit agent state;
- tool dispatch;
- decision contracts;
- bounded execution;
- termination rules;
- retry/recovery;
- reflection;
- trajectory recording;
- repeated-action detection;
- verification;
- budget enforcement;
- failure classification.

## Agent state
A useful state contains:
- goal;
- observations;
- pending action;
- tool results;
- evidence;
- completed steps;
- failures;
- budget counters;
- checkpoints;
- termination reason.

Do not rely on the LLM's context window as the only state store.

## Decision contract
A model decision should resolve to one of:
- `FINAL` — answer is ready;
- `TOOL` — call a specific approved tool;
- `REFLECT` — inspect progress/failure;
- `WAIT` — external dependency is pending;
- `ABORT` — task cannot safely continue.

Invalid decisions must fail closed.

## Termination engineering
An agent needs multiple independent stopping mechanisms:
1. explicit final answer;
2. maximum steps;
3. token budget;
4. tool-call budget;
5. wall-clock deadline;
6. repeated-state detection;
7. repeated-action detection;
8. no-progress threshold;
9. policy denial;
10. unrecoverable error.

A model saying “I am done” is not sufficient evidence of completion.

## Lab 1 — Minimal loop
Build a fake model and two tools. Implement Observe → Decide → Act → Verify.

**Exercise:** Make the model choose a tool based on the current state, not hard-coded task code.

## Lab 2 — Decision schema
Define a typed decision object and reject malformed decisions.

**Failure injection:** return unknown action types, missing tool names and invalid arguments.

## Lab 3 — Tool loop
Build a calculator + knowledge lookup agent. Record every action and result.

## Lab 4 — Termination
Inject an agent that continually requests the same tool. Add repetition detection and hard budgets.

## Lab 5 — Retry vs reasoning
Create transient tool failures and reasoning failures. Retry infrastructure failures; do not blindly retry semantic mistakes.

## Lab 6 — Verification
Give the agent a tool that returns a plausible but incorrect result. Add an independent verifier.

## Lab 7 — Reflection
After a failed verification, let the agent inspect the failure and choose a new action. Bound reflection cycles.

## Lab 8 — Planner/executor
Separate high-level planning from execution. Compare with a single-loop agent.

## Lab 9 — Trajectory replay
Persist trajectories and replay them deterministically using recorded tool results.

## Lab 10 — Adversarial agent
Inject misleading observations, malicious tool results, repeated actions and impossible goals. Prove the runtime remains bounded.

## Detailed exercises
1. Implement the state object.
2. Implement a typed decision contract.
3. Build a tool dispatcher.
4. Add policy checks before execution.
5. Add step/token/tool-call budgets.
6. Add repeated-action fingerprints.
7. Add no-progress detection.
8. Add verification results.
9. Add retry classification.
10. Add reflection with a maximum reflection budget.
11. Add trajectory serialization.
12. Add replay mode.
13. Add cancellation.
14. Add deadline handling.
15. Add final termination reasons.
16. Compare planner/executor vs reactive loops.
17. Measure success per step.
18. Calculate average wasted tool calls.
19. Build a loop-failure taxonomy.
20. Design a recovery strategy for each failure class.

## Failure-first exercises
### Infinite loop
Model repeats `search → search → search`. Detect repeated state/action fingerprints.

### Oscillation
Model alternates between two actions. Detect cycles rather than only identical consecutive actions.

### Premature completion
Model returns FINAL despite missing required evidence. Verification rejects completion.

### Tool-result injection
A tool result contains instructions attempting to alter the goal. Treat the result as untrusted data.

### Retry storm
A permanent failure is retried indefinitely. Add error classification and exponential backoff.

### Budget bypass
Model attempts to claim completion without satisfying the budget/verification contract. Runtime remains authoritative.

## Metrics
Track:
- task success rate;
- successful completion per step;
- average/median steps;
- tool calls/task;
- retries/task;
- reflection cycles;
- verification failures;
- termination reasons;
- p50/p95 runtime;
- token cost;
- failure recovery rate.

## Production architecture
```text
Agent Runtime
 ├── State Store
 ├── Decision Adapter
 ├── Tool Gateway
 ├── Policy Engine
 ├── Budget Manager
 ├── Verifier
 ├── Recovery Manager
 ├── Trajectory/Audit Store
 └── Observability
```

## Industry exercises
**Banking:** research-only account investigation agent with approval-gated actions.

**Cybersecurity:** incident triage loop that gathers evidence, verifies findings and stops before destructive actions.

**Enterprise IT:** troubleshooting agent that retrieves runbooks, executes safe diagnostics and requests approval for changes.

## Interview questions
1. What makes an agent different from a workflow?
2. Why build the raw loop first?
3. Which responsibilities belong to deterministic code?
4. How do you prevent infinite loops?
5. How do you detect oscillation?
6. Why distinguish retry from reasoning?
7. What is trajectory replay?
8. How should verification affect termination?
9. How do you budget an agent?
10. What belongs in agent state?
11. How do you handle a malicious tool result?
12. How do you compare reactive and planner/executor agents?
13. How do you measure agent efficiency?
14. What is a recovery policy?
15. How do you make agent behavior reproducible?

## System-design challenge
Design a raw agent runtime handling 10,000 concurrent tasks with hard step/time/cost budgets, persistent state, tool authorization, verification, replayable trajectories and graceful cancellation.

## Mastery gate
Build an agent that can complete a multi-step task, recover from transient failures, reject malicious observations, prove completion through verification and terminate safely when progress is impossible.

## Gold challenge
Create three agents—reactive, planner/executor and reflective—and run them on the same 100-task benchmark. Compare task success, steps, tool calls, latency, cost, failure recovery and unsafe-action attempts. Defend which architecture is appropriate and why.

## Google Colab
`notebooks/module_14_raw_agent_loop.ipynb` provides a framework-free executable implementation, failure injection, trajectory inspection and benchmark exercises.
