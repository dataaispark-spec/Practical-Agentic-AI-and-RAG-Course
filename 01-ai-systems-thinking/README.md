# Module 1 — AI Systems Thinking & Architecture Decisions

## Module purpose

This module establishes the most important habit in practical AI engineering: **choose the system architecture from the problem and constraints, not from the popularity of a framework**.

The learner will move from a vague business request such as “build an AI assistant” to a defensible architecture with explicit requirements, knowledge needs, action boundaries, quality metrics, operational limits, and failure controls.

## Source curriculum alignment

This chapter is the practical expansion of Module 1 in the source IITM Pravartak curriculum. The source curriculum remains the authority for its original wording, sequencing, and stated scope. The exercises, architecture decision framework, failure lab, and interview preparation below are hands-on extensions.

## Learning outcomes

By the end of the module, the learner can:

1. Decompose an AI problem into users, tasks, data, actions, risks, and constraints.
2. Distinguish a deterministic application, LLM application, RAG system, agent, and multi-agent system.
3. Decide when retrieval, tools, memory, workflow orchestration, or human approval are actually required.
4. Explain core LLM application architecture and control points.
5. Identify quality, latency, reliability, security, privacy, and cost objectives.
6. Produce an Architecture Decision Record (ADR) and defend the trade-offs.
7. Diagnose a bad architecture from observable symptoms.

## The central idea

A production AI system is not “a prompt connected to an LLM.” It is a controlled socio-technical system.

```text
Business goal
    |
    v
Requirements
    |
    +----------------------------+
    |                            |
    v                            v
Knowledge needed             Actions needed
    |                            |
    v                            v
Retrieval / RAG              Tools / APIs
    |                            |
    +-------------+--------------+
                  |
                  v
               Model
                  |
       +----------+----------+
       |          |          |
       v          v          v
   Guardrails  Evaluation  Observability
       |          |          |
       +----------+----------+
                  |
                  v
             Production
```

## 1. Start with the problem, not the framework

For every proposed AI feature, write the following before choosing technology:

| Dimension | Questions |
|---|---|
| User | Who is using the system? |
| Task | What decision or work must be completed? |
| Knowledge | What facts must be available? |
| Freshness | How quickly can the knowledge change? |
| Action | Must the system only answer, or also act? |
| Risk | What happens when it is wrong? |
| Reliability | What availability and failure tolerance are required? |
| Latency | What response-time budget is acceptable? |
| Cost | What cost/request or cost/task is sustainable? |
| Security | What data and operations are sensitive? |
| Human role | Where must a person approve or review? |

### Practical rule

If the task can be solved reliably with normal software, **do not add an LLM just because an LLM is available**.

If the task needs language generation but not external knowledge or actions, a simple LLM application may be enough.

If the answer depends on enterprise knowledge that may change, consider RAG.

If the system must choose and execute tools under constraints, consider an agent.

If multiple independent reasoning roles truly reduce complexity or improve outcomes, consider multi-agent orchestration. Otherwise, a single agent or deterministic workflow is usually easier to operate.

## 2. Architecture ladder

```text
Level 0 — Deterministic software
        |
Level 1 — LLM application
        |
Level 2 — RAG application
        |
Level 3 — Tool-using agent
        |
Level 4 — Stateful / graph-based agent
        |
Level 5 — Multi-agent system
```

The ladder is **not** a maturity ranking. Higher is not automatically better. Complexity must buy measurable value.

### Decision heuristic

```text
Need generation?
  |
  +-- No --> deterministic software
  |
  +-- Yes --> Need external/current knowledge?
                  |
                  +-- No --> LLM application
                  |
                  +-- Yes --> Need grounded retrieval?
                                  |
                                  +-- Yes --> RAG
                                  |
                                  +-- Need to execute actions?
                                           |
                                           +-- No --> RAG application
                                           |
                                           +-- Yes --> Agent/workflow
                                                      |
                                                      +-- Many roles needed?
                                                               |
                                                               +-- No --> single agent
                                                               |
                                                               +-- Yes --> evaluate multi-agent
```

## 3. LLM application internals

At minimum, a production request should have explicit boundaries for:

```text
Request
  |
  v
Input validation
  |
  v
Prompt/context assembly
  |
  v
Model invocation
  |
  v
Output validation
  |
  v
Policy checks
  |
  v
Response + telemetry
```

The model is only one component.

### Why output validation matters

Suppose the model is expected to return:

```json
{
  "priority": "high",
  "reason": "production outage",
  "confidence": 0.91
}
```

The application should not blindly trust free-form text. Validate the structure, allowed values, ranges, and authorization boundaries before downstream use.

## 4. RAG vs fine-tuning vs long context vs agent

| Need | Strong first candidate | Why |
|---|---|---|
| Current/private knowledge | RAG | Injects selected external knowledge at runtime |
| Stable behavior/style/task pattern | Fine-tuning | Changes model behavior rather than knowledge lookup |
| Moderate one-off context | Long context | Simpler when the full context can fit and quality is acceptable |
| Multi-step decisions + actions | Agent/workflow | Adds tool use and controlled iteration |
| Regulated high-risk workflow | Workflow + retrieval + human approval | Makes control and audit explicit |

### Important distinction

RAG is primarily a **knowledge architecture**.

Agents are primarily an **action/decision architecture**.

They can be combined:

```text
User question
     |
     v
Agent decides
     |
     +---- retrieve policy
     +---- query database
     +---- call application API
     +---- ask another component
     |
     v
Grounded response / action
```

## 5. Agent internals

A useful mental model for a tool-using agent is:

```text
                +------------------+
                |      GOAL        |
                +--------+---------+
                         |
                         v
                 Observe state/context
                         |
                         v
                     Decide step
                         |
             +-----------+-----------+
             |                       |
             v                       v
          Answer                 Call tool
                                     |
                                     v
                               Observe result
                                     |
                                     v
                               Update state
                                     |
                                     +----> decide again
```

Production controls are needed around the loop:

- maximum iterations
- tool allowlists
- argument validation
- timeouts
- retries with limits
- budget limits
- authorization
- human approval for sensitive actions
- complete traceability

## 6. Eight production KPIs

Use a balanced scorecard rather than one “accuracy” number.

| KPI | What it tells you | Example measurement |
|---|---|---|
| Task success | Did the system complete the intended task? | % successful tasks |
| Retrieval quality | Did the system find useful evidence? | Recall@K / MRR |
| Groundedness / faithfulness | Is the answer supported by evidence? | evaluator score + citation checks |
| Latency | Is the experience fast enough? | p50/p95/p99 |
| Reliability | Does the service work consistently? | error/retry rate, uptime |
| Cost | Is the workload economically viable? | cost/request or cost/task |
| Safety | Does it resist harmful/unauthorized behavior? | policy violations, injection tests |
| Observability coverage | Can failures be explained? | trace completeness / diagnostic coverage |

These KPIs should be tied to a product requirement, not collected as decorative dashboards.

## 7. Three industry case studies

### Case A — Enterprise policy assistant

**Problem:** employees ask questions about internal policy and procedures.

**Bad design:** send the question to a general-purpose LLM and hope the model remembers current company policy.

**Better baseline:** RAG over approved policy documents with citations and document-version metadata.

**Higher-risk extension:** if the system can initiate an HR or access-management action, introduce explicit tools, authorization checks, audit logs, and human approval where required.

### Case B — Manufacturing maintenance copilot

**Problem:** technicians need answers across manuals, service bulletins, fault codes, and historical maintenance records.

**Architecture:**

```text
Technician
   |
   v
Question + equipment ID
   |
   v
Access / tenant checks
   |
   v
Hybrid retrieval
   |
   +---- manuals
   +---- bulletins
   +---- service history
   |
   v
Reranking / evidence selection
   |
   v
LLM explanation + cited sources
```

**Failure to plan for:** stale manuals, wrong equipment family, missing document versions, and hallucinated repair steps.

### Case C — Financial operations agent

**Problem:** investigate an operational exception, gather evidence, and prepare a recommended next action.

**Key design decision:** separate **recommendation** from **execution**.

```text
Investigate
   |
   v
Retrieve evidence
   |
   v
Analyze
   |
   v
Recommend
   |
   v
Human approval
   |
   v
Authorized execution
```

Do not let a language model become an implicit authorization layer.

## 8. The AI Architecture Decision Engine

The module project is a small decision-support tool that turns requirements into an explainable architecture recommendation.

### Inputs

```text
needs_generation: bool
needs_current_or_private_knowledge: bool
needs_actions: bool
number_of_independent_roles: int
risk_level: low | medium | high
latency_target_ms: int
budget_per_task: float
human_approval_required: bool
```

### Output

```json
{
  "recommended_pattern": "rag_with_workflow",
  "alternatives_considered": ["llm_app", "rag", "agent"],
  "reasons": [
    "private/current knowledge is required",
    "high-risk actions require explicit approval"
  ],
  "complexity_warning": "avoid multi-agent unless measured evidence justifies it"
}
```

### Reference decision logic

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Requirements:
    needs_generation: bool
    needs_knowledge: bool
    needs_actions: bool
    roles: int
    risk: str
    human_approval: bool


def recommend(req: Requirements) -> str:
    if not req.needs_generation:
        return "deterministic_software"

    if not req.needs_knowledge and not req.needs_actions:
        return "llm_application"

    if req.needs_actions:
        if req.roles > 3 and req.risk != "high":
            return "evaluate_multi_agent"
        return "agent_or_workflow"

    if req.needs_knowledge:
        return "rag"

    return "llm_application"
```

The educational point is not the code. It is the **traceable mapping from requirements to architecture**.

## 9. Hands-on exercises

### Exercise 1 — Architecture triage

For each scenario, choose the minimum viable architecture and justify it:

1. Rewrite customer emails into a standard format.
2. Answer employee questions from constantly changing internal policy documents.
3. Check order status from an API and explain the result.
4. Investigate a security alert using several data sources and propose next steps.
5. Coordinate three specialized reasoning roles on a complex research task.

For each answer, record:

```text
Pattern chosen:
Rejected alternatives:
Why:
Biggest risk:
Primary KPI:
```

### Exercise 2 — Architecture diagram

Draw an architecture for an enterprise support assistant. Include:

- user identity
- retrieval
- model
- tool access
- authorization
- evaluation
- observability
- failure handling

### Exercise 3 — Cost/latency trade-off

Assume an architecture has three model calls per task. Propose two alternatives:

- lower latency / higher cost
- lower cost / higher latency

State the business condition under which each is preferred.

### Exercise 4 — Red-team the architecture

Take your own architecture and list at least five ways it could fail or be abused. Map each failure to a control.

## 10. Failure lab

### Failure 1 — “Everything is an agent”

A simple FAQ system is implemented with an agent that repeatedly decides whether to search, summarize, re-search, and re-summarize.

**Observed:** high token usage, unpredictable latency, no meaningful quality improvement.

**Diagnosis path:**

```text
Measure task success
       |
       v
Measure latency + token usage
       |
       v
Compare against deterministic/RAG baseline
       |
       v
Remove unnecessary loop
```

**Lesson:** complexity must be justified by measurable value.

### Failure 2 — RAG without authorization

A user can retrieve documents from a shared index without tenant-level filtering.

**Observed:** correct retrieval, wrong entitlement.

**Lesson:** retrieval quality is not authorization. Security policy must be enforced outside the language model.

### Failure 3 — Agent as authorization layer

The prompt says “only refund orders under policy limits,” but the downstream refund API trusts the agent's decision.

**Observed:** prompt injection or model error results in an unauthorized refund attempt.

**Lesson:** authorization belongs in deterministic policy enforcement around the tool, not in prose instructions alone.

## 11. Debugging method

Use this five-step pattern for AI systems:

```text
1. Symptom
   |
2. Evidence
   |
3. Hypothesis
   |
4. Controlled experiment
   |
5. Fix + regression test
```

Example:

**Symptom:** users report wrong policy answers.

**Evidence:** retrieval traces show relevant chunks are returned, but an older policy version is selected.

**Hypothesis:** document version metadata is not part of ranking/filtering.

**Experiment:** compare retrieval with and without version-aware filtering.

**Fix:** make effective-date/version constraints explicit and add a regression test.

## 12. Architecture Decision Record template

Create `architecture/ADR-001-pattern-selection.md` using:

```markdown
# ADR-001: Select the minimum sufficient AI architecture

## Context

What business problem and constraints are we solving?

## Decision

What architecture pattern did we choose?

## Alternatives considered

Which simpler and more complex options were evaluated?

## Why this decision

What evidence and requirements drove the decision?

## Risks

What can still go wrong?

## Controls

What validation, authorization, observability, and failure handling exist?

## Consequences

What becomes easier and harder because of this choice?

## Revisit triggers

What measured evidence would justify changing the architecture?
```

## 13. System-design interview challenge

### Prompt

> Design an enterprise AI assistant that answers questions from 50 million internal documents, must support current information, must not cross tenant boundaries, and must expose a few read-only business APIs.

### Interview answer structure

1. Clarify requirements.
2. State scale assumptions.
3. Define quality/SLO targets.
4. Draw the high-level architecture.
5. Explain ingestion and retrieval.
6. Explain authorization.
7. Explain model selection and fallbacks.
8. Explain observability.
9. Explain evaluation and regression.
10. Explain scaling and cost controls.
11. Explain failure modes.
12. Defend rejected alternatives.

## 14. Interview bank

### Foundations

1. What problem does an LLM solve well?
2. Why is an LLM not a database?
3. What is the difference between prompting and programming?
4. When is a deterministic workflow better than an agent?
5. What is RAG solving?
6. What is an agent solving?
7. Why does multi-agent architecture add operational complexity?
8. Why should architecture start with requirements?
9. What is an architecture decision record?
10. Why are production AI systems different from demos?

### Intermediate

11. When would you choose RAG instead of fine-tuning?
12. When is long context preferable to retrieval?
13. How do you evaluate retrieval separately from generation?
14. Why can better retrieval still produce a bad answer?
15. How do you prevent an agent loop from running forever?
16. Where should authorization checks live?
17. What should be logged for an AI request?
18. What is p95 latency and why does it matter?
19. What is the difference between task success and answer similarity?
20. How would you design a fallback when a model provider is unavailable?

### Advanced

21. Design a multi-tenant RAG architecture.
22. How would you diagnose a sudden quality regression?
23. How would you reduce cost without reducing task success?
24. How would you make an agent auditable?
25. How would you prove that multi-agent architecture is worth its complexity?
26. How would you handle stale knowledge?
27. How would you enforce tool authorization?
28. How would you design a safe human-in-the-loop boundary?
29. How would you benchmark two retrieval strategies?
30. What evidence would make you replace an agent with a deterministic workflow?
31. How would you design for regional data residency?
32. How would you handle a model that is fast but less reliable?
33. How would you handle a model that is accurate but too expensive?
34. What would you put into an AI incident runbook?
35. How would you demonstrate your architecture choices to an interviewer using GitHub evidence?

## 15. Coding challenge

Implement `architecture_decider.py` with:

- Pydantic or dataclass requirement models
- validation for risk values
- deterministic decision logic
- reasons for the decision
- rejected alternatives
- unit tests for at least 10 scenarios

## 16. Debugging challenge

A student submits an architecture with:

- one unrestricted vector index
- a general-purpose LLM
- direct refund API access
- no timeouts
- no model fallback
- no evaluation dataset
- no trace IDs

The challenge is to identify the seven highest-impact risks, rank them, and propose the smallest safe redesign.

## 17. Mastery gate

The learner passes Module 1 only when they can complete all of the following without copying a reference solution:

```text
[ ] Translate a business problem into technical requirements
[ ] Select the minimum sufficient architecture
[ ] Draw the request/data/action flow
[ ] Explain RAG vs fine-tuning vs long context vs agent
[ ] Define at least five production KPIs
[ ] Identify authorization boundaries
[ ] Write an ADR
[ ] Diagnose a deliberately flawed architecture
[ ] Implement the Architecture Decision Engine
[ ] Add automated tests
[ ] Explain every major trade-off verbally
```

### Interview defense requirement

The learner must be able to explain their repository implementation in 10 minutes:

```text
Problem -> Requirements -> Decision -> Architecture
        -> Implementation -> Failure -> Measurement
        -> Improvement -> Trade-offs
```

## GitHub deliverables

```text
01-ai-systems-thinking/
├── README.md
├── theory/
│   └── architecture-thinking.md
├── diagrams/
│   ├── architecture-ladder.md
│   ├── llm-app.md
│   ├── rag-vs-agent.md
│   └── request-control-loop.md
├── exercises/
│   └── module-1-exercises.md
├── solutions/
├── labs/
│   └── architecture-decision-engine/
│       ├── architecture_decider.py
│       ├── models.py
│       ├── README.md
│       └── tests/
├── interview/
│   ├── questions.md
│   └── system-design.md
├── architecture/
│   └── ADR-001-pattern-selection.md
└── assessment/
    └── mastery-gate.md
```

## What comes next

Module 2 takes the architecture ideas from this chapter and turns them into engineering mechanics with **Python for AI Engineering**: typed interfaces, configuration, HTTP/API clients, async execution, concurrency limits, structured errors, retries, logging, request IDs, and a production-style LLM client.
