# Module 37 — Harness Engineering

## Mission
Build the runtime that turns a capable language model into a reliable agent.

A useful abstraction is:

```text
Agent = Model + Harness + Environment + Tools + State + Policy + Verification
```

The model proposes reasoning and actions. The harness supplies the operating discipline.

## Learning outcomes

By completing this module you can:

1. Explain why model capability alone is not a complete agent runtime.
2. Design a harness boundary around context, state, tools and policy.
3. Implement progressive context disclosure and context-budget management.
4. Integrate reusable skills and sub-agents through explicit contracts.
5. Persist and restore state safely.
6. Enforce policy, budgets, approvals and verification outside model output.
7. Instrument harness behavior for replay and debugging.
8. Compare harness designs and defend trade-offs.

## Harness architecture

```text
MODEL
  ↓
Context / Decision
  ↓
HARNESS CORE
  ├─ state
  ├─ tools
  ├─ policy
  ├─ budget
  ├─ skills
  ├─ memory
  ├─ checkpoints
  ├─ recovery
  └─ telemetry
  ↓
ENVIRONMENT
  ↓
OBSERVATION → VERIFIER
```

## Hands-on lab — AegisAI Agent Harness

Build a reusable harness with a provider-neutral model adapter, context manager, typed tool gateway, deterministic policy layer, persistent state store, budget manager, verifier and telemetry sink.

### Labs

1. Implement the model adapter boundary.
2. Build progressive context loading.
3. Add skill discovery with on-demand skill loading.
4. Add tool registry and policy filtering.
5. Add durable checkpoint/restore.
6. Add replayable event history.
7. Inject stale checkpoint and invalid tool outputs.
8. Measure harness overhead and task success.

## Failure-first cases

Context ordering bugs, missing state, malformed tool output, unauthorized capability exposure, stale checkpoints, tenant leakage and non-deterministic restore.

## Security

The harness is a control boundary. Model outputs, skills, memories, tool results and workspace contents are data; authorization and policy remain deterministic.

## Mastery gate

Demonstrate a model swap without changing policy logic, safe checkpoint recovery, controlled context growth, tool authorization, telemetry coverage and a reproducible debugging trace.
