# Module 41 — Recursive & Self-Improving Agents

**Canonical implementation:** `41-recursive-self-improving-agents/`. Former `36-recursive-self-improving-agents/` is legacy only.

## Mission
Build agents that improve parts of their problem-solving process through controlled experimentation while preserving reproducibility, safety, rollback and independent evaluation.

## Learning outcomes
Define improvement surfaces, create trajectory-derived hypotheses, build candidate experiments, compare baseline/candidate behavior, detect evaluator capture and reward hacking, version changes, enforce bounded recursion, promotion gates, canaries and rollback.

## Architecture
```text
Production Runs → Failure Analysis → Improvement Hypothesis
                                      ↓
                               Candidate Artifact
                                      ↓
                          Sandbox + Independent Verifier
                                      ↓
                       Regression/Security Evaluation
                                      ↓
                           Canary → Promote/Rollback
```

## Labs
1. Prompt improvement with a fixed baseline.
2. Skill improvement.
3. Retrieval improvement.
4. Tool-selection improvement.
5. Harness recovery improvement.
6. Three-candidate independent selection.
7. Self-diagnosis by failure layer.
8. Self-generated tests plus independent tests.
9. Benchmark-gaming/red-team lab.
10. Improvement provenance ledger.
11. Recursive loop with hard iteration/time/token/cost limits.
12. Canary and rollback.

## Exercises
Allow a weak evaluator to be manipulated, then demonstrate evaluator independence. Optimize success while holding security as a hard constraint. Compare improvement quality against experiment cost.

## Measures
Baseline/candidate success, safety regressions, policy violations, cost/latency delta, candidate count, verifier agreement, rollback count and generalization to held-out tasks.

## Security
An agent must never increase its own authority merely by arguing that the increase improves performance. Candidate code executes in an isolated environment and cannot modify the external evaluation authority.

## Mastery gate
Demonstrate baseline → diagnosis → hypothesis → isolated experiment → independent verification → adversarial evaluation → promotion/rollback with an immutable improvement record.
