# Module 36 — Recursive & Self-Improving Agents

## Mission

Build agents that can improve parts of their own **problem-solving process** through controlled experimentation, while preserving reproducibility, safety, rollback and human governance.

The key distinction is:

```text
SELF-IMPROVEMENT
      ≠
UNCONTROLLED SELF-MODIFICATION
```

A production-grade self-improving agent should behave more like an engineer running experiments than like arbitrary code rewriting itself in a loop.

---

## Core model

```text
Goal
 ↓
Current harness
 ↓
Task execution
 ↓
Trajectory
 ↓
Failure / bottleneck analysis
 ↓
Improvement hypothesis
 ↓
Candidate artifact
 ↓
Sandbox experiment
 ↓
Verifier + regression suite
 ↓
Canary
 ↓
Promote / reject / rollback
```

The candidate may modify a prompt, skill, memory policy, router, verifier, tool-selection strategy or harness component. Promotion is always a separate governed operation.

---

# Learning outcomes

You will learn to:

- define recursive improvement precisely
- identify what an agent is allowed to change
- construct improvement hypotheses from trajectories
- build an experiment harness
- compare baseline and candidate behavior
- prevent circular self-improvement loops
- detect reward hacking and benchmark gaming
- maintain versioned improvement artifacts
- implement rollback and kill switches
- evaluate changes across capability, safety, cost and reliability
- design bounded research/coding agents
- understand recursive harness improvement as an engineering problem

---

# 1. What does "self-improving" actually mean?

There are several levels.

| Level | Agent can change | Risk |
|---|---|---|
| L0 | nothing | low |
| L1 | task context | low |
| L2 | memory | moderate |
| L3 | skills/prompts | moderate |
| L4 | routing/tool policy | high |
| L5 | harness code | very high |
| L6 | model/training process | research-grade |

The course treats higher levels as progressively more controlled.

A useful engineering rule:

> The more fundamental the component being changed, the stronger the verification and approval boundary must be.

---

# 2. Improvement hypothesis

Do not let the agent say only:

```text
"I should improve myself."
```

Require a testable hypothesis:

```text
OBSERVATION:
RAG tasks fail when retrieved evidence contains duplicate chunks.

HYPOTHESIS:
Deduplicating candidates before reranking will improve grounded-answer success.

CHANGE:
Add deduplication stage.

EXPECTED EFFECT:
+5% grounded-task success.

REGRESSION RISKS:
Reduced recall for genuinely similar documents.

TEST:
500 fixed evaluation tasks + adversarial duplicates.
```

This converts vague reflection into engineering.

---

# 3. Baseline before improvement

Every improvement experiment needs a baseline.

Record:

```text
agent version
harness version
model version
task distribution
dataset version
environment version
verifier version
configuration
metrics
cost
latency
```

Without a stable baseline, "improvement" is often just anecdotal.

---

# 4. Improvement surfaces

The agent may propose changes at different surfaces:

```text
Prompt
  ↓
Skill
  ↓
Memory policy
  ↓
Retriever
  ↓
Tool selection
  ↓
Planner
  ↓
Verifier
  ↓
Harness
  ↓
Model / training
```

The system should identify the smallest surface capable of addressing the observed failure.

Example:

```text
Failure: agent repeatedly forgets output schema.

Bad response:
replace entire model.

Better response:
strengthen structured output contract + verifier.
```

---

# 5. Experiment harness

Build a controlled runner:

```python
class Experiment:
    def run(self, candidate, tasks, seed): ...
    def evaluate(self, results): ...
    def compare(self, baseline, candidate): ...
    def decide(self, comparison): ...
```

Candidate execution must occur in an isolated environment.

Capture:

```text
task
seed
candidate version
trajectory
verifier output
metrics
errors
cost
latency
side effects
```

---

# 6. Multi-objective improvement

Never optimize only task success.

Evaluate a vector:

```text
capability
correctness
safety
policy compliance
cost
latency
recovery
robustness
```

A candidate should be rejected when:

```text
success ↑
security ↓↓↓
```

even if the aggregate score looks better.

Use explicit hard constraints for non-negotiable properties.

---

# 7. Recursive improvement loop

A bounded recursive loop can be:

```text
for iteration in range(MAX_ITERATIONS):
    observe_failures()
    propose_hypothesis()
    build_candidate()
    evaluate_candidate()
    if passes_gates():
        canary()
    else:
        reject()
```

Required controls:

- maximum iterations
- time budget
- token budget
- monetary budget
- candidate count
- maximum code diff
- approval gates
- rollback
- kill switch

Never implement recursion as an unbounded `while True`.

---

# 8. Preventing circular improvement

A dangerous pattern:

```text
agent A improves planner
 ↓
planner improves evaluator
 ↓
evaluator changes what counts as improvement
 ↓
new evaluator approves planner
```

The agent has effectively changed the rules of the game.

Therefore separate:

```text
SYSTEM UNDER TEST
        |
        v
EXTERNAL EVALUATION AUTHORITY
```

The evaluator should not be freely mutable by the candidate being evaluated.

---

# 9. Research-agent pattern

For research tasks:

```text
Question
 ↓
Hypotheses
 ↓
Search
 ↓
Evidence collection
 ↓
Experiment
 ↓
Result
 ↓
Verifier
 ↓
Conclusion
 ↓
Next hypothesis
```

The agent should preserve evidence and failed hypotheses, not only its final conclusion.

This turns research into an inspectable trajectory rather than a polished narrative.

---

# 10. Coding-agent pattern

For software engineering:

```text
Issue
 ↓
Inspect repository
 ↓
Form hypothesis
 ↓
Modify code
 ↓
Run tests
 ↓
Inspect failures
 ↓
Revise
 ↓
Regression suite
 ↓
Patch / PR artifact
```

A self-improving coding harness can learn better procedures for debugging, testing and repository navigation without automatically granting itself unrestricted production write access.

---

# 11. Self-debugging

Teach the agent to classify failure before proposing a change:

```text
MODEL FAILURE
RETRIEVAL FAILURE
TOOL FAILURE
POLICY FAILURE
STATE FAILURE
VERIFIER FAILURE
ENVIRONMENT FAILURE
HARNESS FAILURE
```

Otherwise the agent may repeatedly "fix" the wrong layer.

Example:

```text
Tool timeout
 ↓
agent changes prompt
 ↓
timeout remains
```

Correct diagnosis:

```text
execution-layer failure
```

---

# 12. Self-generated tests

An advanced agent may propose tests for its own candidate.

That is useful but insufficient.

Use:

```text
agent-generated tests
        +
independent regression suite
        +
adversarial tests
        +
human-selected tests
```

Otherwise the agent can accidentally define a benchmark it is already guaranteed to pass.

---

# 13. Benchmark gaming

Intentionally test:

- training/evaluation contamination
- test memorization
- evaluator manipulation
- reward hacking
- environment exploitation
- selective failure reporting
- benchmark-specific overfitting

A candidate should be evaluated on held-out and adversarial tasks.

---

# 14. Improvement provenance

Every promoted change should answer:

```text
Who proposed it?
What evidence motivated it?
Which trajectory exposed the problem?
What changed?
Which tests passed?
Which tests failed?
Who/what approved it?
What version replaced?
How can it be rolled back?
```

Create an immutable improvement record.

---

# 15. Build project — AegisAI Research Harness

Implement:

```text
GoalManager
TrajectoryAnalyzer
HypothesisGenerator
CandidateBuilder
ExperimentRunner
Verifier
RegressionSuite
PromotionGate
VersionRegistry
RollbackManager
```

APIs:

```text
analyze(run_id)
propose_improvement(observations)
run_experiment(candidate_id)
compare(candidate_id, baseline_id)
promote(candidate_id)
rollback(version)
```

The candidate cannot directly call `promote()` without satisfying the gate.

---

# 16. Hands-on challenge sequence

### Challenge 1 — Prompt improvement

Find a repeatable failure and improve only the prompt.

### Challenge 2 — Skill improvement

Convert repeated successful reasoning into a versioned skill.

### Challenge 3 — Retrieval improvement

Use trajectory evidence to improve retrieval.

### Challenge 4 — Tool policy

Reduce unnecessary tool calls without reducing task success.

### Challenge 5 — Harness improvement

Modify execution logic to improve recovery.

### Challenge 6 — Recursive experiment

Allow the agent to propose three candidates and select the best candidate using an independent evaluator.

---

# 17. Failure laboratory

### Failure A — Infinite recursion

Remove iteration limits.

Expected lesson: budget controls are mandatory.

### Failure B — Evaluator capture

Allow the candidate to modify the evaluator.

Expected lesson: evaluation authority must be independent.

### Failure C — Reward hacking

Use a weak reward and observe shortcut behavior.

### Failure D — Regression hiding

Optimize average success while ignoring security failures.

### Failure E — Candidate explosion

Allow unlimited candidate generation.

Measure compute and cost growth.

### Failure F — Version confusion

Run active tasks against a changing skill/harness version.

Expected lesson: execution version pinning matters.

### Failure G — False self-diagnosis

Inject a tool failure and observe whether the agent incorrectly modifies its prompt.

---

# 18. Metrics

Track:

```text
baseline_success
candidate_success
absolute_gain
relative_gain
safety_regressions
policy_violations
cost_delta
latency_delta
candidate_count
experiment_time
rollback_count
verifier_agreement
```

Also measure:

```text
improvement_quality = durable_gain / experiment_cost
```

Treat this as an engineering metric, not a universal scientific law.

---

# 19. Production architecture

```text
              Production Runs
                    |
                    v
             Trajectory Store
                    |
                    v
             Failure Analyzer
                    |
                    v
          Improvement Hypothesis
                    |
                    v
              Candidate Lab
             /      |       \
        sandbox  verifier  adversarial
             \      |       /
                    v
            Independent Evaluator
                    |
              +-----+-----+
              |           |
            reject       canary
                          |
                       promote
                          |
                       registry
                          |
                    production
```

Production and experimentation must have separate credentials and trust boundaries.

---

# 20. Safety architecture

Minimum controls:

- immutable baseline
- isolated candidate execution
- external evaluation authority
- bounded recursion
- version pinning
- human approval for high-impact changes
- kill switch
- rollback
- audit trail
- credential separation
- no self-granting permissions
- no evaluator self-modification

A particularly important rule:

> **An agent must never be able to increase its own authority merely by arguing that the increase would improve performance.**

---

# 21. Interview bank

### Conceptual

1. What is a self-improving agent?
2. How is self-improvement different from self-modification?
3. What can safely be improved first?
4. Why do we need a baseline?
5. Why is evaluation authority important?

### Engineering

6. How would you build a candidate experiment runner?
7. How do you version improvement artifacts?
8. How do you prevent infinite recursive loops?
9. How do you isolate candidate code?
10. How do you detect benchmark gaming?

### Safety

11. What if the agent improves task success but weakens security?
12. How do you prevent an agent from modifying its evaluator?
13. How do you handle self-generated tests?
14. When is human approval required?
15. How do you roll back a harmful improvement?

### Research / RL

16. How can trajectories generate improvement hypotheses?
17. How does a verifier support recursive improvement?
18. How does this connect to agentic RL?
19. What is reward hacking in a self-improvement loop?
20. How would you evaluate whether an improvement generalizes?

---

# 22. System-design challenge

**Design a self-improving enterprise coding agent.**

Constraints:

- 100,000 tasks/month
- candidate improvements generated automatically
- independent evaluation environment
- no production credentials in experiments
- security regressions are hard failures
- five-minute rollback target
- full trajectory provenance
- human approval for harness-code changes

Defend:

- experiment isolation
- candidate representation
- evaluation authority
- regression strategy
- promotion criteria
- rollback
- budget controls
- audit architecture

---

# 23. Mastery gate

You pass when you can demonstrate:

1. A measurable baseline.
2. A trajectory-derived failure diagnosis.
3. A concrete improvement hypothesis.
4. An isolated candidate experiment.
5. Independent verification.
6. Adversarial evaluation.
7. Multi-objective comparison.
8. Promotion gating.
9. Versioned deployment.
10. Tested rollback.

## Gold challenge

Give the agent a benchmark where it can increase its score by manipulating the evaluator. The agent must discover or encounter the exploit, the independent evaluator must reject the shortcut, and the final system must produce an auditable record explaining why the candidate was not promoted.

---

## Frontier connection

This module is the bridge between **continual harnesses** and more advanced agentic-RL/research-agent systems. Modern research harnesses increasingly make the runtime, tools, skills, memory and execution process explicit objects of experimentation. The course keeps the central engineering discipline intact:

```text
Hypothesis → Experiment → Verification → Promotion
```

not:

```text
Agent says it improved → trust agent → deploy
```

The next module moves from recursive improvement into **computer-use and always-on enterprise digital workers**, where the agent operates across applications and persistent environments rather than only within a text/tool sandbox.
