# Module 32 — Harness Engineering

## Mission

Build the runtime that turns a capable language model into a reliable agent.

A useful abstraction is:

```text
Agent = Model + Harness + Environment + Tools + State + Policy + Verification
```

The model proposes reasoning and actions. The harness supplies the operating discipline.

## What is a harness?

The harness is the software surrounding the model that manages:

- context assembly
- state
- tools
- skills
- sub-agents
- memory
- filesystem/workspace
- execution
- policy
- budgets
- checkpoints
- retries
- approvals
- telemetry
- recovery
- evaluation hooks

This module deliberately builds a small harness before comparing it with modern agent runtimes.

## Architecture

```text
                    MODEL
                      |
             +--------+--------+
             |                 |
             v                 v
          Context           Decision
             |                 |
             +--------+--------+
                      |
                      v
                HARNESS CORE
       +----------+---+---+----------+
       |          |       |          |
     State      Tools   Policy     Budget
       |          |       |          |
       +----------+-------+----------+
                      |
                      v
                 Environment
                      |
                      v
                  Observation
                      |
                  Verifier
```

## 1. Context engineering

Context is a managed resource, not an infinite string.

A good harness decides:

- what enters context
- when it enters
- what gets summarized
- what remains in durable state
- what is retrieved on demand
- what is never exposed

Use progressive disclosure:

```text
small routing context
       ↓
skill metadata
       ↓
load full skill only when needed
       ↓
retrieve task-specific evidence
```

## 2. Skills

A skill is procedural knowledge the agent can load when useful.

Skill contract:

```text
name
purpose
when_to_use
inputs
procedure
constraints
verification
examples
```

Skills should be versioned and testable. Do not blindly let an agent rewrite production skills without evaluation.

Modern systems such as Hermes expose skills as on-demand knowledge and allow agent-created skills. This is an excellent case study for progressive disclosure and procedural memory, but the course implementation remains framework-independent.

## 3. Tool registry

Every tool should expose:

```text
name
description
input schema
output schema
authorization scope
side-effect class
timeout
retry policy
cost estimate
```

Classify tools:

```text
READ_ONLY
REVERSIBLE_WRITE
IRREVERSIBLE_WRITE
PRIVILEGED
```

This classification feeds policy decisions.

## 4. Policy engine

Never put all safety logic in a prompt.

```python
class PolicyDecision:
    allowed: bool
    reason: str
    requires_human: bool


def authorize(tool, principal, arguments):
    ...
```

Examples:

- read customer profile → allowed
- modify profile → conditional
- issue refund → approval
- rotate production credential → blocked

## 5. Durable state

Separate:

- ephemeral loop state
- session state
- durable memory
- artifacts
- audit log
- configuration

A harness should be able to restart without losing the authoritative workflow state.

## 6. Checkpoints

Checkpoint at state transitions, especially around external side effects.

```text
prepare action
   ↓
checkpoint
   ↓
execute side effect
   ↓
checkpoint result
```

This reduces ambiguity during crash recovery.

## 7. Sub-agent orchestration

A harness may delegate work:

```text
Supervisor
   |
   +--> researcher
   +--> coder
   +--> verifier
```

But delegation introduces:

- context transfer cost
- synchronization complexity
- duplicated work
- failure propagation
- authorization questions
- cost multiplication

Every sub-agent should receive a bounded objective and budget.

## 8. MCP as an adapter boundary

MCP can extend a harness without embedding every integration into its core.

Teach the distinction:

```text
Harness
   |
   +-- native tool
   |
   +-- MCP adapter
   |       |
   |       +-- external tool server
   |
   +-- API adapter
```

Expose the minimum required MCP surface. Tool discovery is capability discovery and therefore part of the security boundary.

## 9. Harness observability

Trace at least:

```text
run_id
session_id
agent_id
parent_run_id
iteration
model call
context size
selected tool
arguments hash
policy decision
tool latency
observation
verifier result
budget remaining
checkpoint id
final outcome
```

Never log credentials or unrestricted sensitive tool arguments.

## 10. Build project — AegisAI Harness

Implement:

```text
Harness.run(task)
Harness.resume(run_id)
Harness.pause(run_id)
Harness.cancel(run_id)
Harness.inspect(run_id)
```

Components:

```text
ContextManager
StateStore
ToolRegistry
SkillRegistry
PolicyEngine
BudgetManager
CheckpointStore
ExecutionEngine
Verifier
TraceSink
```

## 11. Compare modern designs

Study Hermes Agent's combination of memory, skills, Bot Mode, MCP, delegation, scheduled work, hooks and programmatic tool calling. Use the system to ask architectural questions rather than copying its implementation.

Study Prime Agent's argument for a **Continual Harness**: the harness itself can become an object of improvement rather than a static collection of prompts and tools.

Study persistent-agent products such as Grok Bot as a reference for the product implications of durable identity, own-computer environments, autonomous work and approval points.

## 12. Failure lab

Break:

- state persistence
- tool authorization
- context selection
- skill loading
- sub-agent budget propagation
- checkpoint ordering
- resume logic
- cancellation
- MCP tool filtering
- audit trace correlation

## Interview bank

1. What is a harness?
2. Why isn't the model the whole agent?
3. What should be deterministic?
4. How do skills differ from memory?
5. Why is progressive disclosure useful?
6. How do you safely expose MCP tools?
7. What state must survive a process restart?
8. How do you recover after an external side effect?
9. How do you prevent sub-agent cost explosions?
10. How would you design a harness for 10,000 concurrent agents?

## Mastery gate

Demonstrate a working harness that supports tools, policies, skills, state, checkpoints, budgets, traces and resumability. Then explain which responsibilities belong to the harness rather than the model.
