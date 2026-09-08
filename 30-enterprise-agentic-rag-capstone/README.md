# Module 30 — Enterprise Agentic RAG Capstone

## Mission
Integrate Modules 1–29 into a production-shaped enterprise Agentic RAG platform. This capstone is the first complete AegisAI system before the dedicated Knowledge Engineering/GraphRAG and frontier autonomy track in Modules 31–43.

## Learning outcomes

By completing this capstone you can:

1. Translate an enterprise goal into a task contract, risk profile and architecture.
2. Integrate governed RAG, retrieval, tools, agent loops, memory and stateful workflows.
3. Enforce authentication, authorization, tenant isolation, budgets and human approval.
4. Verify evidence and consequential actions independently of model output.
5. Instrument the full system for quality, latency, cost, security and debugging.
6. Evaluate releases with regression and adversarial test suites.
7. Design deployment, rollback and incident-recovery paths.
8. Defend the architecture and trade-offs in a production system-design review.

## Reference flow

```text
User / Event
  ↓
Task + Risk Classification
  ↓
Policy / Identity / Budget
  ↓
Agent / Workflow
  ├─ RAG / Retrieval
  ├─ Memory
  └─ Tools / MCP
  ↓
Verification
  ↓
Telemetry / Evaluation
  ↓
Approved Action or Grounded Answer
```

## Hands-on labs

1. Define the enterprise task and acceptance criteria.
2. Connect tenant-aware RAG and evidence citations.
3. Add typed tools and approval-gated mutations.
4. Add bounded agent execution and checkpoints.
5. Add memory with provenance and expiry.
6. Add observability and evaluation.
7. Add failure injection and recovery.
8. Build CI/CD release gates and rollback.

## Failure-first benchmark

Retrieval miss, stale knowledge, tenant leakage, malformed tool request, provider timeout, unauthorized action, duplicate mutation, false verification, budget exhaustion and failed deployment rollback.

## Required scorecard

Task success, groundedness, citation correctness, tool correctness, safety violations, recovery success, p50/p95 latency, cost per successful task and trace completeness.

## Deliverables

Architecture ADR, application implementation, executable Colab notebook, tests, failure report, evaluation report, security threat model, cost report and deployment/release manifest.

## Mastery gate

The learner must demonstrate a complete governed Agentic RAG workflow, reproduce and recover from failures, measure the system, and defend why each component exists and what simpler alternative was rejected.
