# Module 43 — Frontier Graph-RAG Agentic Capstone

**Canonical implementation:** `43-frontier-graph-rag-agentic-capstone/`. Former `38-frontier-agentic-rag-capstone/` is legacy only.

## Mission
Build AegisAI as a production-style platform for bounded enterprise work, integrating GraphRAG, hybrid retrieval, tools/MCP, loops, harnesses, memory/skills, durable execution, environments/verifiers, computer use, evaluation, cost, security, governance and controlled self-improvement.

## Learning outcomes
Design a task contract and risk profile; retrieve authorized graph/vector evidence; execute bounded tool/agent workflows; persist and recover state; verify consequential outcomes; use computer environments safely; evaluate quality/cost/safety; and promote improvements only through independent gates.

## Reference architecture
```text
User/Event → Task + Risk → Policy/Identity/Budget
                         ↓
              Agent/Harness/Workflow
              ↙        ↓         ↘
          GraphRAG    Memory     Tools/MCP/UI
              ↘        ↓         ↙
                  Verification
                  ↙         ↘
              Approval     Recovery
                  ↘         ↙
                    Result
                       ↓
             Evaluation + Audit
                       ↓
          Sandbox → Canary → Rollback
```

## Capstone phases
1. Foundation/task contract.
2. Graph + vector retrieval and evidence.
3. Agent loop, tools, budgets and termination.
4. Harness, durable state, memory and skills.
5. MCP/business integrations and approvals.
6. Computer-use sandbox.
7. Long-running workers and recovery.
8. Environment/verifier evaluation.
9. Controlled self-improvement.
10. Production deployment and incident response.

## Labs / exercises
Build the same enterprise scenario through progressively stronger controls. Inject retrieval miss, stale graph edge, tenant leakage, malformed tool request, provider timeout, duplicate mutation, false verification, budget exhaustion, stale UI state, poisoned memory/skill and bad self-improvement. For each failure produce detection, containment, recovery and regression evidence.

## Required scorecard
Recall@K, multi-hop accuracy, groundedness, citation correctness, task success, tool correctness, safety violations, recovery rate, p50/p95 latency, cost/success, trace completeness, resume success, computer-use verified success and improvement regression delta.

## Security/governance
Deterministic policy surrounds model proposals. Graphs and memories are evidence, not authority. Tenant/ACL boundaries, DLP, approval gates, immutable audit, kill switches, credential separation and independent verification remain mandatory.

## Deliverables
Architecture ADR, implementation, executable Colab, tests, failure report, evaluation report, threat model, cost report, deployment manifest, recovery matrix and controlled-improvement record.

## Mastery gate
Demonstrate a complete governed Agentic Graph-RAG workflow, reproduce and recover from failures, measure quality/cost/safety, defend simpler alternatives and prove that no self-improvement path can silently increase authority.
