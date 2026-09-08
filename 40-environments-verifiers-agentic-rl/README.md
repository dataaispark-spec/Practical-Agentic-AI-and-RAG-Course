# Module 40 — Environments, Verifiers & Agentic RL

**Canonical implementation:** `40-environments-verifiers-agentic-rl/`. Former `35-environments-verifiers-agentic-rl/` is legacy only.

## Mission
Move from agents that merely generate responses to agents that act inside measurable environments and receive executable feedback.

## Learning outcomes
Design reproducible task environments, trajectories, deterministic/model-assisted verifiers, reward signals, reset/replay semantics, held-out evaluation and safe improvement loops. Understand why reward is an engineering signal, not truth.

## Architecture
```text
Task → Environment → Agent/Policy → Trajectory → Verifier → Score/Reward
                                      ↑                    ↓
                               Replay/Artifacts ← Evaluation
```

## Labs
1. Environment contract and seeded reset.
2. Task vs environment separation.
3. Structured trajectory recorder.
4. Deterministic verifier.
5. Model-assisted semantic verifier.
6. Hybrid verifier.
7. Reward-hacking laboratory.
8. Reproducible replay.
9. Offline vs online improvement comparison.
10. Multi-verifier adjudication.
11. Held-out/adversarial evaluation.
12. Sandbox security and reset isolation.
13. AegisAI training/evaluation environment.

## Exercises
Delete a test, manipulate an evaluation artifact, exploit a simulator shortcut or persuade a model judge without completing the task. Strengthen the verifier and prove legitimate solutions still pass.

## Measures
Success rate, verifier pass rate, false accept/reject rate, pass@k, steps, cost/success, latency/success, unsafe-action rate and recovery rate.

## Security
Sandbox untrusted execution, isolate filesystem/network access, separate training/evaluation/production credentials, prevent evaluation contamination and treat environment escapes as critical failures.

## Mastery gate
Execute and replay a task, verify it independently, demonstrate reward hacking against a weak reward, harden the verifier and defend why higher reward does not necessarily mean a better agent.
