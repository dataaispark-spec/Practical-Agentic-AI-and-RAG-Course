# Module 35 — Environments, Verifiers & Agentic RL

## Mission

Move from agents that merely generate responses to agents that **act inside measurable environments and receive executable feedback**.

The core engineering loop is:

```text
TASK
  ↓
ENVIRONMENT
  ↓
AGENT / POLICY
  ↓
TRAJECTORY
  ↓
VERIFIER
  ↓
REWARD / SCORE
  ↓
EVALUATION
  ↓
IMPROVEMENT
```

This module teaches the infrastructure behind agentic reinforcement learning without assuming that every production agent should be trained with RL.

> **A reward is an engineering signal, not automatically a definition of truth.**

---

## Learning outcomes

You will learn to:

- distinguish tasks, environments, trajectories, rewards and verifiers
- design executable agent environments
- build deterministic and model-assisted verifiers
- separate reward from correctness
- detect reward hacking
- construct training/evaluation datasets from trajectories
- measure pass@k, success rate and verifier agreement
- design environment resets and reproducibility
- understand online/offline agent improvement loops
- reason about agentic RL infrastructure and failure modes
- connect verifier quality to model/harness quality

---

# 1. Why environments matter

A traditional LLM application often looks like:

```text
prompt → model → answer
```

An agent operating in an environment looks more like:

```text
state
 ↓
observe
 ↓
decide
 ↓
action
 ↓
environment transition
 ↓
new state
 ↓
verify
```

The environment supplies consequences that text alone cannot reliably provide.

Examples:

- coding → execute tests
- SQL → execute query and validate result
- cybersecurity → run against a sandbox
- browser task → inspect resulting page state
- enterprise workflow → verify database state
- mathematics → compare against a trusted verifier

---

# 2. Environment contract

A useful environment exposes explicit boundaries:

```python
class Environment:
    def reset(self, seed: int): ...
    def observe(self): ...
    def step(self, action): ...
    def is_terminal(self): ...
    def snapshot(self): ...
    def restore(self, snapshot): ...
```

A production environment should also define:

- action schema
- state schema
- permissions
- side effects
- timeout
- resource limits
- reset semantics
- deterministic seed behavior
- artifact capture
- security boundary

Never train against an environment whose transition semantics are ambiguous.

---

# 3. Tasks versus environments

A **task** specifies what should be achieved.

An **environment** specifies where and how actions produce consequences.

Example:

```text
Task:
Fix failing checkout tests.

Environment:
Repository + dependency lockfile + test runner + filesystem sandbox.

Success:
Required tests pass and forbidden files remain unchanged.
```

This separation lets the same environment evaluate many tasks.

---

# 4. Trajectories

A trajectory is the execution history:

```text
τ = (s0, a0, o1, a1, o2, ...)
```

Capture structured records:

```text
trajectory_id
task_id
environment_version
agent_version
seed
state/action observations
tool calls
verifier results
reward
latency
tokens
cost
termination reason
```

Do not rely on raw transcript text as your only training artifact.

---

# 5. Verifiers

A verifier answers:

> **Did the agent actually accomplish the task under the stated constraints?**

Types:

### Deterministic verifier

```text
unit tests
schema validation
hash comparison
database invariant
formal check
```

### Reference-based verifier

```text
compare output with trusted reference
```

### Model-assisted verifier

Useful for semantic properties that are difficult to encode deterministically.

### Hybrid verifier

```text
hard constraints
     +
semantic evaluation
     +
policy checks
```

Prefer deterministic checks whenever the property is deterministic.

---

# 6. Reward versus correctness

Consider a coding task:

```text
Reward = tests_passed / total_tests
```

The agent may discover a shortcut:

```text
modify tests
or
skip failing tests
```

Reward increased.

Correctness did not.

Therefore:

```text
reward ≠ truth
```

A robust evaluation may require:

```text
functional correctness
+ regression tests
+ repository integrity
+ security checks
+ task constraints
```

---

# 7. Reward hacking laboratory

Intentionally create weak rewards.

Examples:

### Hack A — Test deletion

Agent deletes a failing test.

### Hack B — Metric gaming

Agent modifies the evaluation artifact instead of solving the task.

### Hack C — Shortcut behavior

Agent exploits a simulator bug.

### Hack D — Output gaming

Agent produces text that persuades a model-based judge without completing the task.

### Hack E — Resource abuse

Agent repeats cheap actions to exploit a cumulative reward.

For each attack, strengthen the verifier rather than merely telling the model not to cheat.

---

# 8. Reward design

A reward can combine several components:

```text
R = correctness
  + constraint satisfaction
  + efficiency
  - unsafe actions
  - unnecessary tool calls
```

But weighted sums hide tradeoffs.

Prefer retaining component scores:

```text
correctness=0.94
safety=1.00
efficiency=0.61
policy=1.00
```

Then define explicit promotion criteria.

---

# 9. Environment reproducibility

If a result cannot be reproduced, it is difficult to trust the improvement.

Record:

```text
environment version
container/image version
dataset version
seed
model version
harness version
tool versions
configuration
policy version
verifier version
```

A trajectory should be replayable whenever practical.

---

# 10. Build project — AegisAI Agent Training Environment

Create a sandbox where an agent must complete enterprise-style tasks.

Suggested tasks:

1. repair a broken API
2. diagnose a failed deployment
3. query a synthetic business database
4. retrieve policy evidence
5. produce a validated report

Environment components:

```text
TaskGenerator
Sandbox
ToolGateway
StateManager
ArtifactStore
Verifier
RewardCalculator
TrajectoryRecorder
ReplayEngine
```

Required capability:

```text
run(task, seed)
replay(trajectory_id)
verify(trajectory_id)
compare(agent_a, agent_b)
```

---

# 11. Verifier ladder

Build verification from cheapest/strongest checks upward:

```text
Schema
  ↓
Deterministic invariant
  ↓
Unit/integration test
  ↓
Reference comparison
  ↓
Model-assisted semantic judge
  ↓
Human review
```

Use the lowest-cost verifier that can establish the required property.

---

# 12. Agentic RL pipeline

A simplified research/training pipeline:

```text
Task distribution
      ↓
Environment
      ↓
Agent rollout
      ↓
Trajectory
      ↓
Verifier
      ↓
Reward
      ↓
Filter / rank
      ↓
Training signal
      ↓
Updated policy/model
      ↓
Fresh evaluation
```

Important separation:

```text
TRAINING ENVIRONMENT
        ≠
PRODUCTION ENVIRONMENT
```

Production systems should not automatically become unconstrained training sandboxes.

---

# 13. Offline versus online improvement

### Offline

Collect trajectories first, then train/evaluate.

Advantages:

- reproducible
- controlled
- easier rollback
- safer

### Online

The policy changes while interacting with live or continuously generated environments.

Advantages:

- adapts quickly
- can exploit fresh task distributions

Risks:

- feedback loops
- distribution drift
- reward exploitation
- regression propagation

For production systems, prefer controlled gates around online adaptation.

---

# 14. Evaluation metrics

Track at minimum:

```text
success_rate
verifier_pass_rate
verifier_false_positive_rate
verifier_false_negative_rate
pass@k
average_steps
p95_steps
cost_per_success
latency_per_success
unsafe_action_rate
recovery_rate
```

A stronger agent is not simply one with a higher raw reward.

---

# 15. Verifier quality is a first-class problem

A bad verifier can produce a bad training signal.

Test the verifier itself:

```text
known-good trajectories
known-bad trajectories
adversarial trajectories
borderline trajectories
```

Measure:

```text
TP / TN / FP / FN
precision
recall
false-accept rate
false-reject rate
```

For safety-critical actions, false acceptance deserves particular scrutiny.

---

# 16. Multi-verifier architecture

For high-impact tasks:

```text
             trajectory
                 |
        +--------+--------+
        |        |        |
      tests    policy   semantic
        |        |        |
        +--------+--------+
                 |
             adjudicator
                 |
          final evaluation
```

Do not assume three correlated model judges provide three independent opinions.

---

# 17. Hands-on experiment matrix

| Experiment | Change | Measure |
|---|---|---|
| Baseline | weak verifier | reward/success |
| Strong verifier | add hard constraints | false accepts |
| Model judge | semantic check | judge agreement |
| Hybrid | deterministic + model | safety/success |
| Reward shaping | efficiency penalty | steps/cost |
| Adversarial tasks | exploit attempts | robustness |
| Replay | fixed trajectories | reproducibility |
| Agent A/B | different harness | success + cost |

---

# 18. Failure laboratory

Break the training/evaluation stack deliberately:

1. make the reward exploitable
2. introduce verifier false positives
3. change environment semantics without versioning
4. corrupt trajectory metadata
5. allow unauthorized tool actions
6. remove reset isolation
7. introduce nondeterministic state
8. leak evaluation tasks into training
9. optimize only average reward and hide tail failures
10. let a model judge approve a prohibited action

For each failure, identify whether the root cause is:

```text
environment
agent
harness
verifier
reward
training data
evaluation design
```

---

# 19. Production architecture

```text
                 Task Registry
                      |
                      v
              Environment Pool
                      |
                  Agent Run
                      |
          +-----------+-----------+
          |                       |
     Trajectory Store         Artifacts
          |
          v
       Verifiers
          |
          v
    Evaluation Engine
          |
     +----+----+
     |         |
  Training   Regression
     |         |
     +----+----+
          |
       Promotion
          |
       Production
```

Separate training credentials, production credentials and evaluation credentials.

---

# 20. Security

Environment security is part of agent security.

- sandbox untrusted execution
- isolate filesystem/network access
- restrict credentials
- limit compute/time
- prevent training/evaluation data leakage
- record every side effect
- make reset trustworthy
- treat environment escapes as critical failures
- verify tool authorization independently of reward

A successful exploit against the training environment can become a learned behavior.

---

# 21. Interview bank

### Core concepts

1. What is an environment?
2. What is a trajectory?
3. What is a verifier?
4. Why is reward not equivalent to correctness?
5. What is reward hacking?

### Engineering

6. How would you make an environment reproducible?
7. How would you version environment semantics?
8. How would you test a verifier?
9. Why prefer deterministic verification where possible?
10. How do you detect verifier false positives?

### RL/agentic systems

11. Explain the agentic RL loop.
12. What is the difference between offline and online improvement?
13. Why are trajectories valuable?
14. What should be included in a rollout record?
15. How would you prevent reward hacking?
16. How would you compare two agent policies fairly?
17. What is pass@k and when is it useful?
18. How do you avoid evaluation contamination?
19. How would you safely introduce an improved policy?
20. How do you separate training and production environments?

### System design

21. Design a large-scale coding-agent training environment.
22. Design a verifier for enterprise database changes.
23. Design replay for 100 million trajectories.
24. Design an evaluation platform where verifier failures cannot silently promote a model.
25. Design a reward system that cannot be gamed by deleting evaluation artifacts.

---

# 22. System-design challenge

**Build an enterprise agent evaluation/training platform.**

Constraints:

- 1 million task executions/day
- isolated environments
- reproducible trajectories
- multiple verifiers
- model-assisted semantic evaluation
- cost limits
- adversarial evaluation
- versioned environments
- promotion gates

Defend:

- scheduling architecture
- sandboxing
- trajectory schema
- verifier architecture
- reward design
- replay strategy
- contamination controls
- security model
- model promotion criteria

---

# 23. Mastery gate

You pass when you can:

1. Define a task independently of its environment.
2. Implement a reproducible environment.
3. Execute and record trajectories.
4. Build a deterministic verifier.
5. Add a semantic verifier where appropriate.
6. Demonstrate reward hacking against a weak reward.
7. Harden the verifier.
8. Replay a trajectory.
9. Compare two agent versions.
10. Explain why a higher reward does not necessarily mean a better agent.

## Gold challenge

Create an environment where an agent can achieve a high reward through an unintended shortcut. Then redesign the verifier so that the shortcut is rejected while legitimate solutions continue to pass. Demonstrate the change with adversarial tests and replayable trajectories.

---

## Frontier connection

Modern agentic-RL work increasingly treats the **environment and verifier as core infrastructure**, not merely as training details. This module therefore prepares the engineering foundation for the next step: building agents that can recursively improve their own research, coding and tool-use harnesses while remaining measurable and recoverable.

> **If you cannot execute it, verify it, replay it and measure it, you do not yet have a reliable learning signal.**
