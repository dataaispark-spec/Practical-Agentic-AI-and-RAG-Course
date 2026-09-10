# Module 41 — Recursive Self-Improvement: Theory

## Safe improvement model
Self-improvement means selecting and deploying a better artifact, not giving an agent unrestricted ability to rewrite itself. Improvement surfaces include prompts, retrieval, tool routing, skills, memory policy, planning, recovery and harness components.

## Experimental lifecycle
`BASELINE → FAILURE MINING → HYPOTHESIS → CANDIDATE → SANDBOX → INDEPENDENT EVALUATION → ADVERSARIAL TEST → CANARY → PROMOTE/ROLLBACK`.

## Causal discipline
Change one meaningful variable where practical, retain the baseline, use paired task sets, preserve evaluator independence and separate optimization data from held-out evaluation. Record experiment identity and provenance.

## Evaluator capture
If the candidate can change the evaluator, benchmark, test fixtures or scoring rules, the optimization target is compromised. The evaluation authority must remain outside candidate control.

## Recursive boundary
Bound recursion by depth, wall-clock time, experiment count, token/compute budget and monetary cost. Each generation must inherit the same or stricter authority constraints.

## Authority invariant
**Performance improvement can never authorize privilege expansion.** A candidate must not grant itself credentials, bypass policy, weaken verification or modify the trusted evaluator.

## Promotion economics
Measure quality delta per experiment cost and require meaningful improvement rather than accepting every statistically noisy gain. Use shadow/canary deployment and automatic rollback thresholds.

## Exercises
Create three competing retrieval optimizers; detect benchmark gaming; design evaluator separation; prove a candidate cannot modify the verifier; implement canary rollback after a safety regression.
