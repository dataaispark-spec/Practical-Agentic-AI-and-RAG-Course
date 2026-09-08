# Module 41 — Recursive & Self-Improving Agents

## Mission
Build agents that can improve parts of their problem-solving process through controlled experimentation while preserving reproducibility, safety, rollback and governance.

## Learning outcomes

By completing this module you can:

1. Define bounded self-improvement and distinguish it from uncontrolled self-modification.
2. Identify which agent artifacts may be changed and under what authority.
3. Convert trajectories and failures into testable improvement hypotheses.
4. Build a baseline/candidate experiment harness.
5. Evaluate capability, safety, reliability and cost changes together.
6. Detect benchmark gaming, evaluator gaming and contamination.
7. Version candidate prompts, skills, memories, routers and harness components.
8. Implement promotion gates, canaries, kill switches and rollback.
9. Prevent recursive improvement loops from becoming unbounded.
10. Defend a governed self-improvement architecture.

## Improvement loop

```text
Goal → current harness → trajectory → bottleneck
→ improvement hypothesis → candidate artifact
→ sandbox experiment → verifier/regression → canary
→ promote/reject → monitor → rollback
```

## Hands-on lab — Research Agent Harness

Implement controlled mutation of a prompt, skill, retrieval policy or routing policy. Run paired baseline/candidate evaluations on fixed and held-out cases. Block promotion when quality, safety, cost or reliability gates regress.

### Failure-first cases

Evaluator gaming, contaminated benchmark data, runaway recursion, hidden capability regression, reward hacking and rollback failure.

### Metrics

Paired improvement delta, safety delta, regression rate, experiment cost, rollback success and promotion rejection rate.

## Security

Candidate artifacts are untrusted until independently evaluated. The improving agent may propose changes but must not grant itself new permissions or bypass promotion gates.

## Mastery gate

Produce a reproducible improvement experiment, reject a harmful candidate, demonstrate rollback and explain the external controls that keep self-improvement bounded.
