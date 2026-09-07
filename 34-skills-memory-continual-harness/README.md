# Module 34 — Skills, Memory & Continual Harnesses

## Mission

Teach agents to accumulate useful procedural knowledge and durable state without turning memory into an uncontrolled garbage dump.

## Three distinct concepts

### Memory

Facts, experiences and state that may persist across tasks.

### Skill

Reusable procedural knowledge describing how to perform a class of work.

### Harness configuration

The runtime rules controlling tools, policies, budgets, state and execution.

These must have separate lifecycle and security policies.

## Progressive disclosure

A strong pattern is:

```text
Task
 ↓
Skill index
 ↓
Select relevant skill
 ↓
Load full procedure
 ↓
Execute
 ↓
Verify
```

Loading every skill into every context wastes tokens and can increase confusion.

Hermes Agent is a useful current case study because it treats skills as on-demand knowledge, supports persistent memory and allows agent-created skills. The course treats those features as architectural patterns rather than dependencies.

## Memory architecture

```text
                 Memory Router
                     |
       +-------------+-------------+
       |             |             |
   working        episodic       semantic
   state          history        knowledge
       |             |             |
       +-------------+-------------+
                     |
                 governance
```

Every memory needs:

- source
- timestamp
- confidence/provenance
- owner/tenant
- retention policy
- sensitivity classification
- deletion policy

## Skill lifecycle

```text
DISCOVER
   ↓
DRAFT
   ↓
TEST
   ↓
EVALUATE
   ↓
PUBLISH
   ↓
MONITOR
   ↓
DEPRECATE / ROLLBACK
```

An agent should not automatically promote an unverified self-generated skill into production authority.

## Continual harness

A continual harness allows experience to influence future execution.

```text
Task
 ↓
Trajectory
 ↓
Failure / success analysis
 ↓
Candidate improvement
 ↓
Offline evaluation
 ↓
Canary
 ↓
Promotion or rollback
```

The improvement artifact may be:

- skill revision
- memory update
- routing rule
- prompt adjustment
- tool selection rule
- sub-agent configuration
- model selection

## Build project — Skill & Memory Manager

Implement:

```text
SkillStore
MemoryStore
SkillEvaluator
MemoryPolicy
VersionRegistry
PromotionGate
RollbackManager
```

The agent should be able to propose an improvement but not bypass evaluation.

## Failure laboratory

1. Store contradictory memories.
2. Store stale policy as memory.
3. Let an agent create a skill that silently weakens a security control.
4. Promote a skill without evaluation.
5. Leak tenant data through shared memory.
6. Allow unbounded memory growth.
7. Modify a skill during an active run.

## Interview questions

1. How is memory different from RAG?
2. When should knowledge become a skill?
3. How do you prevent stale memories from dominating current facts?
4. How do you govern agent-created skills?
5. What is a continual harness?
6. How would you roll back a harmful learned behavior?
7. How do you isolate memory across tenants?

## Mastery gate

Demonstrate a versioned skill and memory system in which the agent can propose an improvement, the evaluator can reject it, and a previous known-good version can be restored automatically.
