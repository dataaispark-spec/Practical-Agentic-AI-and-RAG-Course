# Module 37 — Harness Engineering

**Canonical implementation:** `37-harness-engineering/`. Former `32-harness-engineering/` is legacy only.

## Mission
Build the runtime that turns a capable model into a reliable agent. `Agent = Model + Harness + Environment + Tools + State + Policy + Verification`.

## Learning outcomes
Design context management, state, tools, skills, sub-agents, memory, workspace, checkpoints, retries, approvals, budgets, telemetry and recovery as explicit deterministic control surfaces.

## Architecture
```text
Task Contract → Identity/Tenant → Context Builder → Model Adapter
                                      ↓
                                Action Proposal
                                      ↓
                           Policy + Budget + Approval
                                      ↓
                              Tool/MCP Gateway
                                      ↓
                              Environment/API
                                      ↓
                    Verify → State/Checkpoint → Trace
```

## Labs
1. Provider-neutral model adapter.
2. Priority-aware enterprise context builder.
3. Typed tool gateway with RBAC and idempotency.
4. Ephemeral vs durable state.
5. Policy and budget hooks.
6. Context-window management benchmark.
7. Provider fallback and recovery.
8. Versioned skills and safe extension surfaces.
9. Minimal vs guarded vs durable harness benchmark.
10. Red-team prompt injection, malicious tool output and tenant mismatch.
11. Deterministic replay.
12. Cancellation, deadlines, circuit breakers and audit.
13. Coding-agent harness.
14. Customer-support harness with approval-gated refund.
15. Framework-light vs framework-heavy architecture review.

## Exercises
Break context ordering, tool validation, persistence, policy hooks, fallback, cancellation, tenant isolation, checkpoint recovery and budget enforcement. Identify the first broken invariant.

## Measures
Task success, tool-call precision, context tokens, p95 latency, cost/task, recovery success, safety violations and replay divergence.

## Security
Never put all safety logic in a prompt. MCP discovery is capability discovery and therefore part of the trust boundary. Never log credentials or unrestricted sensitive tool arguments.

## Mastery gate
Build AegisAI Harness v1 with tools, policies, skills, durable state, checkpoints, budgets, traces and resumability, then defend what belongs in deterministic code rather than the model.
