# Module 40 — Environments, Verifiers & Agentic RL

## Mission
Move from agents that merely generate responses to agents that act inside measurable environments and receive executable feedback.

## Learning outcomes

By completing this module you can:

1. Distinguish tasks, environments, trajectories, rewards and verifiers.
2. Design reproducible executable agent environments.
3. Build deterministic and model-assisted verifiers.
4. Separate reward signals from correctness and policy.
5. Detect reward hacking and verifier gaming.
6. Collect trajectories as training/evaluation data.
7. Measure verified success, pass@k and verifier agreement.
8. Design environment resets and held-out evaluation.
9. Explain offline/online improvement loops and agentic RL infrastructure.
10. Defend when RL is justified and when direct engineering is preferable.

## Core loop

```text
TASK → ENVIRONMENT → AGENT/POLICY → TRAJECTORY
      → VERIFIER → REWARD/SCORE → EVALUATION → IMPROVEMENT
```

## Hands-on lab — Agent Training Environment

Build a deterministic enterprise task environment with reset/observe/step/terminal/snapshot contracts, action schemas, a deterministic verifier, reward decomposition, trajectory storage and held-out test generation.

### Failure-first cases

Reward hacking, verifier gaming, leaked evaluation tasks, non-reproducible resets, distribution shift and unsafe actions.

### Metrics

Verified success, raw reward, reward–verifier correlation, pass@k, held-out performance, safety violations, environment determinism and evaluator agreement.

## Security

The verifier and environment must be isolated from the agent's ability to alter evaluation truth. Training/evaluation data must be separated to reduce leakage and benchmark gaming.

## Mastery gate

Build and run an environment, demonstrate a reward hack, detect it with independent verification, and explain why reward is only a proxy for the desired outcome.
