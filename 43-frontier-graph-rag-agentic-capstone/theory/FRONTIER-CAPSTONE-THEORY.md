# Module 43 — Frontier Graph-RAG Agentic Capstone: Architecture & Theory

## Mission
Integrate the course without collapsing boundaries. AegisAI is a governed socio-technical system: model reasoning is probabilistic; execution, identity, policy, budgets, verification and audit are deterministic controls.

## System layers
1. task/risk contract;
2. identity and tenant boundary;
3. GraphRAG/vector evidence;
4. loop and harness;
5. tools/MCP/computer environment;
6. durable state and memory/skills;
7. independent verifier;
8. evaluation/observability;
9. controlled improvement;
10. deployment/governance.

## End-to-end invariant
`UNTRUSTED INPUT → EVIDENCE → PROPOSAL → POLICY → BOUNDED EFFECT → INDEPENDENT VERIFICATION → AUDITABLE COMMIT`.

Graphs, memories, retrieved documents and tool outputs remain evidence. None may independently authorize action.

## Progressive architecture
Begin with deterministic workflow. Add RAG only where retrieval improves quality. Add GraphRAG when relationship/multi-hop evidence justifies it. Add agents when decision branching justifies autonomy. Add durable workers when tasks exceed process lifetime. Add computer use only where structured interfaces are insufficient. Add self-improvement only after independent evaluation exists.

## Final evaluation
Use paired fixed and adversarial task sets. Report retrieval quality, task success, safety violations, verifier outcomes, recovery, latency, cost and improvement deltas. Compare simple, baseline-agent, guarded-agent and frontier architectures so complexity must earn its place.

## Failure engineering
At least one failure from every layer: retrieval, graph temporal state, policy, tool, loop, durability, memory/skill, verifier, UI, evaluator and improvement pipeline. Each failure requires detection, containment, recovery, regression and residual-risk evidence.

## Graduation challenge
Design AegisAI for a high-volume enterprise workload. Defend architecture, SLOs, tenancy, threat model, cost model, rollback, incident response and why each autonomous capability is necessary rather than fashionable.
