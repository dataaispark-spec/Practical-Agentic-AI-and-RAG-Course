# Module 33 — Long-Running & Autonomous Agents

## Mission

Move from request/response agents to durable workers that can operate for hours or days while remaining bounded, observable, recoverable and governable.

The key abstraction is:

```text
Long-running Agent
= Goal + Durable State + Loop + Environment + Tools
  + Policy + Budgets + Verification + Recovery
```

A large context window is **not** durable execution. Persistence requires an authoritative state model outside the model context.

Modern persistent-agent systems make this a practical engineering problem. The course studies systems such as Hermes Agent, Prime Agent and Grok Bot as architectural case studies—not as product tutorials.

---

## Learning outcomes

Build and defend a worker that supports:

- durable goals, tasks and runs
- leases and heartbeats
- deadlines and multidimensional budgets
- checkpoints and resumability
- bounded retries
- idempotent side effects
- pause/resume/cancel
- human escalation and approval
- scheduled execution
- artifact management
- crash and worker-failure recovery
- stale-state detection
- policy re-validation
- audit reconstruction

---

# 1. Why long-running agents are different

A chat agent can fail by producing a bad answer. A persistent worker can:

- repeat an external action
- accumulate stale state
- consume an unbounded budget
- continue after the user changes their mind
- act with credentials after authorization changes
- create duplicate side effects after restart
- optimize activity instead of the actual goal
- operate against an environment that has changed since the last observation

Therefore lifecycle engineering becomes part of correctness.

---

# 2. Five different identities

Never collapse these into one `agent_session` object.

```text
GOAL
  desired business outcome

TASK
  bounded unit of work

RUN
  durable execution instance

ATTEMPT
  one execution attempt

CHECKPOINT
  authoritative recoverable state
```

Example:

```text
Goal: produce quarterly security report
Task 17: collect endpoint findings
Run 17A: current execution
Attempt 4: after a worker restart
Checkpoint C91: 83/100 endpoints processed
```

This separation makes billing, debugging, retries and recovery tractable.

---

# 3. Durable job lifecycle

```text
CREATED
  ↓
QUEUED
  ↓
RUNNING
  ↓
CHECKPOINTED
  ├── PAUSED
  ├── WAITING_APPROVAL
  ├── WAITING_EXTERNAL
  ├── RETRYING
  ├── FAILED
  └── COMPLETED
```

Cancellation is explicit:

```text
RUNNING → CANCELLING → CANCELLED
```

Every transition should record:

```text
actor
previous_state
next_state
reason
timestamp
correlation_id
checkpoint_id
policy_version
```

The state machine—not the LLM—is authoritative.

---

# 4. Worker leases and heartbeats

A worker should periodically prove it is alive and retain ownership only while its lease is valid.

```text
Worker A
   |
   +-- claim task
   +-- lease
   +-- heartbeat
   +-- heartbeat
   X crash

lease expires
   ↓
Worker B claims task
```

Important parameters:

```text
lease_duration
heartbeat_interval
renewal_deadline
stale_threshold
max_attempts
```

A heartbeat proves liveness, not correctness. A worker can be alive and completely stuck.

Therefore track both:

```text
liveness
+
progress
```

---

# 5. Idempotency and uncertain side effects

The hardest recovery problem is often not remembering what the model thought. It is knowing whether an external action actually happened.

Example:

```text
agent → send_invoice()
external system succeeds
network response is lost
agent sees timeout
agent retries
```

Without idempotency, the invoice may be sent twice.

Use a stable logical operation ID:

```text
operation_id = hash(run_id + logical_action_id)
```

Where supported, pass it downstream as an idempotency key.

For irreversible actions:

```text
prepare
→ policy
→ approval
→ checkpoint
→ execute
→ reconcile
→ checkpoint receipt
→ verify
```

If outcome is uncertain, **reconcile before retrying**.

---

# 6. Checkpoint architecture

A checkpoint must contain enough authoritative information to resume without guessing.

Example:

```json
{
  "run_id": "run-2048",
  "state": "RUNNING",
  "completed_items": ["host-1", "host-2"],
  "pending_items": ["host-3", "host-4"],
  "budget_remaining": {
    "seconds": 742,
    "tokens": 18000,
    "usd": 1.82,
    "tool_calls": 73
  },
  "policy_version": "policy-12",
  "last_verified_at": "2026-09-07T12:00:00Z"
}
```

Separate durable state from ephemeral model context.

Store large artifacts separately and reference them by content/version IDs.

---

# 7. Context compaction

Long-running agents eventually outgrow useful context.

Use:

```text
recent observations
        +
active task state
        +
verified facts
        +
retrieved evidence
        +
compressed history
```

Do not summarize away authoritative facts without provenance.

Rule:

> Compress narrative history; preserve state, evidence, decisions and unresolved risks.

A good experiment compares:

```text
full-history context
vs
summary-only
vs
state + selective retrieval
```

Measure task success, token cost and factual consistency.

---

# 8. Waiting is a first-class state

A mature autonomous worker does not keep thinking while waiting for an external event.

Examples:

```text
WAITING_APPROVAL
WAITING_WEBHOOK
WAITING_DOCUMENT
WAITING_PAYMENT
WAITING_SCHEDULE
```

Preferred architecture:

```text
persist state
→ release worker
→ receive event
→ resume from checkpoint
```

This avoids expensive polling loops and reduces duplicate work.

---

# 9. Approval gates

Human approval must survive process restarts.

```text
agent proposes action
       ↓
policy evaluates
       ↓
requires approval
       ↓
WAITING_APPROVAL
       ↓
human approves/rejects
       ↓
resume / terminate
```

Approval records should include:

- principal
- action hash
- arguments or secure reference
- policy version
- expiration
- timestamp
- decision

An old approval should not automatically authorize a materially changed action.

---

# 10. Change-of-mind semantics

Persistent autonomy requires explicit revocation semantics.

Questions:

- Can the user revoke a goal?
- What happens to queued actions?
- What happens to actions already in flight?
- Can completed side effects be compensated?
- What state remains for audit?

Cancellation is a business operation, not merely `task.cancel()`.

A useful model is:

```text
REVOKED GOAL
    ↓
stop new work
    ↓
cancel safe pending actions
    ↓
reconcile in-flight actions
    ↓
retain audit history
```

---

# 11. Goal drift

Long-running agents can optimize the wrong proxy.

```text
Goal:
find the best supplier

Bad metric:
number of suppliers researched

Result:
agent becomes extremely busy
but does not become more useful
```

Track explicit progress:

```text
goal_metric
acceptance_criteria
remaining_work
confidence
blocking_issue
last_verified_progress
```

At each major iteration ask:

1. What changed?
2. What evidence proves progress?
3. What remains?
4. Did the objective or constraints change?

---

# 12. Multidimensional budgets

A durable agent should not have only a token limit.

```text
Time budget
Token budget
Tool-call budget
Financial budget
Risk budget
Human-attention budget
External API quota
```

Example:

```text
max_runtime = 4h
max_llm_cost = $5
max_tool_calls = 500
max_privileged_actions = 3
max_retries_per_tool = 3
```

Hard budget exhaustion should produce a deterministic transition such as:

```text
RUNNING → PAUSED
```

or:

```text
RUNNING → ESCALATED
```

Do not ask the model whether it is allowed to exceed a hard system budget.

---

# 13. Recovery matrix

| Failure | Recovery |
|---|---|
| model timeout | bounded retry |
| worker crash | resume checkpoint |
| tool timeout | retry / alternate tool |
| lease expiry | reclaim task |
| malformed action | reject + re-plan |
| uncertain side effect | reconcile before retry |
| budget exhausted | pause/escalate |
| policy version changed | re-authorize |
| knowledge changed | revalidate evidence |
| verifier failure | bounded correction loop |
| external dependency unavailable | wait/event-driven retry |

Recovery is part of the architecture, not merely exception handling.

---

# 14. Scheduled autonomy

Scheduled execution changes the threat model.

```text
human prompt
   ↓
agent executes

versus

scheduler
   ↓
autonomous agent
   ↓
external side effect
```

The second design needs explicit:

- owner
- scope
- expiration
- schedule
- budget
- approval policy
- allowed tools
- audit trail
- kill switch

A scheduled task must never become an accidental permanent authority grant.

---

# 15. Build project — Durable Autonomous Worker

Create:

```text
33-long-running-agents/lab/
```

Suggested structure:

```text
lab/
  domain/
    models.py
    state_machine.py
    policies.py
  runtime/
    worker.py
    lease.py
    scheduler.py
    checkpoint.py
    recovery.py
  tools/
    registry.py
    idempotency.py
  evaluation/
    scenarios.py
    metrics.py
  tests/
```

Implement:

```text
create_goal()
create_task()
start_run()
claim_run()
heartbeat()
checkpoint()
pause()
resume()
cancel()
recover_stale_runs()
verify_milestone()
```

Required APIs:

```text
POST /runs
POST /runs/{id}/pause
POST /runs/{id}/resume
POST /runs/{id}/cancel
GET  /runs/{id}
GET  /runs/{id}/events
```

---

# 16. Hands-on experiment matrix

Run the same workload under:

| Experiment | Fault / condition |
|---|---|
| A | normal completion |
| B | worker crash after tool call |
| C | lost tool response |
| D | lease expiration |
| E | context compaction |
| F | budget exhaustion |
| G | policy change during run |
| H | new evidence invalidates conclusion |
| I | delayed human approval |
| J | cancellation during external action |
| K | duplicate queue delivery |
| L | stale worker continues after lease loss |

Measure:

```text
completion rate
recovery rate
duplicate side effects
mean recovery time
cost/run
checkpoint overhead
verification failures
human escalations
```

---

# 17. Failure laboratory

### Failure A — Duplicate execution

Remove idempotency and simulate a lost response.

### Failure B — Split brain

Allow two workers to own one task.

### Failure C — Lost progress

Delete the latest checkpoint and observe recovery.

### Failure D — Goal drift

Change the scoring function so the agent optimizes activity instead of outcome.

### Failure E — Infinite autonomy

Remove runtime and tool-call budgets.

### Failure F — Stale policy

Change authorization rules while a run is paused, then resume it.

### Failure G — Stale knowledge

Modify the knowledge source while the agent is working.

### Failure H — Zombie worker

Stop heartbeats while allowing execution to continue.

For every failure document:

```text
symptom
root cause
invariant violated
containment
repair
regression test
```

---

# 18. Production architecture

```text
                    Scheduler / Event Bus
                             |
                             v
                       Run Dispatcher
                             |
                    +--------+--------+
                    |                 |
                Worker Pool       Approval Queue
                    |
                    v
               Harness Core
          +---------+---------+
          |         |         |
       State     Tools      Policy
          |         |         |
          +----+----+---------+
               |
         Checkpoint Store
               |
         Durable Database
               |
       Audit / Trace Store
```

Infrastructure concerns:

- durable queue
- transactional state store
- lease/lock mechanism
- checkpoint storage
- event bus
- policy service
- secrets management
- observability
- kill switch
- replay/debug tooling
- artifact store

---

# 19. Security model

Long-running autonomy increases blast radius.

Threats:

- persistent prompt injection
- poisoned memory
- stale authorization
- credential exposure
- scheduled abuse
- tool escalation
- unattended side effects
- compromised external systems
- runaway cost
- cross-run data leakage

Controls:

```text
least privilege
short-lived credentials
policy re-checks
approval gates
budget ceilings
sandboxing
memory provenance
immutable audit logs
kill switch
```

Never assume a one-time user authorization remains valid forever.

---

# 20. Observability

Every run should be reconstructable.

Minimum trace fields:

```text
run_id
parent_run_id
attempt_id
iteration
state transition
checkpoint_id
model call
context size
selected tool
action hash
policy decision
external receipt
verifier result
budget remaining
worker_id
lease version
final outcome
```

Useful derived metrics:

```text
progress / minute
cost / successful outcome
recovery success rate
mean time to recovery
side-effect duplication rate
approval latency
stale-run rate
```

---

# 21. Frontier case studies

### Hermes Agent

Study persistent knowledge, skills, scheduled automations, Bot Mode, delegation and programmatic tool calling. Ask what persistence primitive enables each feature and what new failure mode it introduces.

### Prime Agent

Study persistent harness state, recoverable sessions, autonomous goals, heartbeats and the idea that the harness itself can become an object of improvement.

### Grok Bot

Study the product-level implications of always-on agents, persistent identity, computer environments, memory and human approval points.

The engineering question is:

> What durable-system primitive makes the capability possible, and what control is required because of it?

---

# 22. System-design challenge

Design an enterprise autonomous research worker that can:

```text
receive a goal
→ research for up to 24 hours
→ call approved tools
→ persist evidence
→ wait for external events
→ resume automatically
→ request human approval before publication
→ publish only after verification
```

Specify:

- state machine
- queueing
- worker leases
- checkpoint format
- context strategy
- tool policy
- budget policy
- verification
- recovery
- observability
- security
- disaster recovery

Defend every choice and identify the strongest failure mode in your design.

---

# 23. Interview bank

### Conceptual

1. What makes an agent long-running?
2. Why is a large context window not equivalent to durable state?
3. Distinguish goal, task, run, attempt and checkpoint.
4. What is a lease?
5. Why are heartbeats insufficient for correctness?
6. Why must waiting be modeled as state?

### Coding

7. Implement an idempotency key.
8. Implement a lease with expiry.
9. Implement checkpoint/resume logic.
10. Implement bounded durable retry.
11. Implement cancellation-safe worker execution.
12. Build a stale-run recovery worker.

### Debugging

13. Two workers execute one task. Find the race.
14. A resumed task repeats a payment. Diagnose the missing invariant.
15. A worker is alive but makes no progress. What telemetry do you inspect?
16. A paused run resumes under a new security policy. What should happen?
17. A tool succeeds but its response is lost. Design reconciliation.

### Architecture

18. Design 100,000 scheduled agents.
19. Design multi-day research agents.
20. Design durable agents across regions.
21. Design a kill switch for thousands of active agents.
22. How do you prevent autonomous cost explosions?
23. How do you prevent stale permissions?
24. How would you make execution replayable?

---

# 24. Mastery gate

You pass only when the implementation demonstrates:

- durable goal/task/run state
- worker leasing
- heartbeat handling
- checkpointing
- crash recovery
- pause/resume/cancel
- idempotent tool execution
- multidimensional budgets
- approval gates
- milestone verification
- audit reconstruction

## Gold challenge

Kill the worker at random points during execution. Restart it repeatedly. The final business outcome must remain correct **without duplicate irreversible side effects**.

Then change the authorization policy while the job is paused and prove that resume re-checks authorization.

That is the real long-running-agent test.

---

# 25. Key principle

> **Autonomy is not the absence of control. Mature autonomy is control that survives time, failure and interruption.**

Next: **Module 34 — Skills, Memory & Continual Harnesses**, where the agent begins to retain useful knowledge and improve its operating procedures while keeping self-modification behind measurable evaluation gates.
