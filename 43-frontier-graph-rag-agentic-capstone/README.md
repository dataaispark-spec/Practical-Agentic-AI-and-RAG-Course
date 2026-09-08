# Module 43 — Frontier Graph-RAG Agentic Capstone

## AegisAI — Autonomous Enterprise Intelligence Platform

## Mission
Integrate the course into one bounded enterprise system combining retrieval, knowledge graphs, tools, agents, loops, harnesses, memory, skills, MCP, multi-agent coordination, long-running execution, computer use, environments, verifiers, evaluation, cost controls, security, governance, CI/CD and controlled self-improvement.

## Learning outcomes

By completing this capstone you can:

1. Architect the complete AegisAI platform from an enterprise goal and risk profile.
2. Combine vector retrieval, knowledge-graph retrieval and hybrid evidence selection.
3. Operate tools/MCP behind deterministic authorization and policy controls.
4. Run bounded agent loops inside a reusable harness.
5. Persist goals, state, memory, skills and checkpoints safely.
6. Coordinate specialist workers only when benchmark evidence justifies them.
7. Verify intermediate and final outcomes with independent evidence.
8. Operate long-running and computer-use workflows with approval boundaries.
9. Evaluate quality, security, latency, recovery and cost as one release contract.
10. Introduce controlled self-improvement with external promotion and rollback gates.
11. Produce an auditable architecture/evaluation/security evidence pack.
12. Defend every major design decision in a production system-design review.

## Reference architecture

```text
USER / EVENT
    ↓
TASK + RISK CLASSIFICATION
    ↓
POLICY / IDENTITY / TENANT / BUDGET
    ↓
HARNESS
    ├── loop
    ├── state
    ├── memory
    ├── skills
    └── verification
    ↓
RETRIEVAL LAYER
    ├── vector
    ├── lexical
    ├── knowledge graph
    └── hybrid/reranked
    ↓
TOOLS / MCP / COMPUTER USE
    ↓
ENVIRONMENT
    ↓
AUDIT + OBSERVABILITY + EVALUATION
    ↓
CONTROLLED IMPROVEMENT / RELEASE GATE
```

## Hands-on capstone sequence

1. Define task contracts and risk tiers.
2. Build the retrieval and graph evidence layer.
3. Integrate policy-governed tools/MCP.
4. Add bounded loop + harness.
5. Add durable state, memory and skills.
6. Add verifier and failure recovery.
7. Add multi-agent escalation only where useful.
8. Add long-running worker and computer-use path in a synthetic environment.
9. Add production evaluation, cost and governance gates.
10. Run a coordinated chaos benchmark.
11. Demonstrate rollback from a bad knowledge update, skill, routing change or harness candidate.

## Failure benchmark

Inject retrieval miss, stale/poisoned graph evidence, tenant leakage, malformed tool calls, authorization denial, duplicate side effect, worker crash, stale checkpoint, verifier disagreement, reward hacking, UI drift, cost explosion and unsafe autonomous action.

For every failure record: observable symptom → first causal failure → containment → recovery → regression test.

## Required scorecard

Task success, groundedness, citation correctness, graph evidence quality, verifier pass rate, safety violations, recovery success, p50/p95 latency, cost per successful task, duplicate-effect rate, audit completeness and improvement-gate accuracy.

## Deliverables

Architecture ADR, executable reference implementation, Colab deep-practice notebook, test suite, failure/chaos report, evaluation report, security threat model, cost analysis, deployment/release manifest and portfolio-ready system-design presentation.

## Mastery gate

Pass only when the complete system can demonstrate grounded retrieval, governed tool use, bounded autonomy, durable recovery, independent verification, measurable economics, security containment and controlled improvement without relying on model output as the final authority.
