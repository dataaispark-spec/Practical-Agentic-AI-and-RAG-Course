# Module 31 Exercises — Loop Engineering

## Exercise 1 — Minimum sufficient loop

Build the smallest loop that can complete a multi-step research task. Start with a deterministic workflow, then introduce model-controlled branching only where the path is genuinely uncertain.

Deliverables:
- architecture diagram
- state model
- termination policy
- benchmark against deterministic baseline

## Exercise 2 — Budget controller

Implement independent budgets for:
- iterations
- model calls
- tool calls
- tokens
- wall time
- estimated cost

The controller must produce a structured reason when any budget is exhausted.

## Exercise 3 — Loop detector

Create tests for:
- identical repeated actions
- alternating actions
- repeated state fingerprints
- legitimate repeated actions that should not be blocked

Explain the false-positive trade-off.

## Exercise 4 — Retry vs replan

Build a simulator with transient errors and semantic failures. Demonstrate that:
- transient errors trigger bounded retry
- semantic failure triggers a new plan
- retries do not consume the reasoning budget unless your architecture explicitly chooses that policy

## Exercise 5 — Verification ladder

Compare:
1. no verifier
2. deterministic verifier
3. model-based verifier
4. hybrid verifier

Measure task success, cost, latency and false acceptance.

## Exercise 6 — Crash recovery

Inject a process crash after an external side effect but before checkpoint persistence. Design idempotency or reconciliation so a resumed run does not duplicate the side effect.

## Exercise 7 — Reflection economics

Compare 0, 1, 2 and 3 reflection rounds. Determine the point at which additional reflection no longer produces sufficient verified improvement.

## Exercise 8 — Harness case study

Compare the primitive loop you built with the architectural ideas documented by Hermes and Prime Agent. Identify which responsibilities belong in the runtime rather than in the model prompt.
