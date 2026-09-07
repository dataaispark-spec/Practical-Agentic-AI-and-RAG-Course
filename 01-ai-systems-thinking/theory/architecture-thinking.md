# Architecture Thinking — Module 1 Theory

## 1. AI engineering is systems engineering

A language model is a component. The product is the system around it.

A useful decomposition is:

```text
Input
  -> validation
  -> context/data acquisition
  -> model reasoning/generation
  -> output validation
  -> policy enforcement
  -> side effects (if any)
  -> telemetry
```

The key engineering question is not “which model is best?” in isolation. It is “which system design produces the required outcome under the business constraints?”

## 2. Probabilistic component, deterministic boundary

LLMs may produce different outputs for the same semantic request. Production systems still need contracts. The control layer turns probabilistic behavior into bounded application behavior.

| Layer | Typical control |
|---|---|
| Input | schema validation, authentication |
| Context | retrieval policy, tenant filters |
| Model | model selection, prompt/version control |
| Output | structured parsing, validation |
| Action | authorization, allowlists, approvals |
| Reliability | timeout, retry budget, fallback |
| Operations | traces, metrics, alerts |
| Learning loop | evaluation datasets, regression tests |

## 3. Complexity budget

Every new subsystem creates a new failure surface.

```text
LLM app
  + retrieval
  + reranker
  + tools
  + memory
  + planner
  + multi-agent coordination
  + observability
  + security
       = more capability
       + more complexity
       + more latency paths
       + more operational cost
```

Use additional complexity only when the expected business value can be measured.

## 4. Requirement-to-architecture mapping

Convert prose requirements into architectural primitives.

```text
"Must know current policy"
      -> retrieval + freshness/versioning

"Must read order status"
      -> authenticated read-only tool

"Must issue refunds"
      -> authorized action tool + deterministic policy + approval boundary

"Must support 24x7"
      -> timeouts + fallback + monitoring + incident response

"Must never leak tenant data"
      -> identity propagation + authorization before retrieval/tool use
```

## 5. RAG architecture thinking

RAG is not one feature. It is a pipeline:

```text
Sources
  -> parsing
  -> normalization
  -> chunking
  -> metadata
  -> embeddings/indexing
  -> candidate retrieval
  -> filtering/reranking
  -> context assembly
  -> generation
  -> citation/groundedness checks
```

A low-quality answer can originate at any stage. “The model hallucinated” is often an incomplete diagnosis.

## 6. Agent architecture thinking

An agent introduces a decision loop.

```text
Goal
  -> observe state
  -> select next action
  -> execute tool/workflow step
  -> observe result
  -> update state
  -> repeat or finish
```

The loop must have explicit boundaries:

- iteration/time budget
- allowed tools
- valid argument schemas
- authorization
- error handling
- state limits
- escalation policy

## 7. Multi-agent skepticism

Multiple agents may help when the task has separable responsibilities that can be independently evaluated or coordinated. They hurt when they create ceremony without measurable gains.

Before introducing multi-agent orchestration, benchmark a simpler baseline.

```text
Baseline task success = 84%
Baseline cost/task    = $0.06
Baseline p95 latency  = 2.1s

Multi-agent task success = 85%
Multi-agent cost/task    = $0.41
Multi-agent p95 latency  = 9.8s

Conclusion: more agents != better architecture
```

## 8. Production questions to ask first

### Correctness

What counts as success? What must be grounded?

### Reliability

What can fail, and how should the system degrade?

### Security

Which data may be read? Which actions may be executed?

### Observability

Can we reconstruct why the system produced the result?

### Economics

What is the cost ceiling per user/task/workflow?

### Change management

How will model, prompt, retrieval, and tool changes be evaluated before release?

## 9. Architecture review checklist

```text
[ ] Business objective is explicit
[ ] Users and permissions are explicit
[ ] Knowledge sources are identified
[ ] Freshness requirements are identified
[ ] Actions are listed separately from answers
[ ] High-risk actions have deterministic controls
[ ] Quality metrics are defined
[ ] Latency budget is defined
[ ] Cost budget is defined
[ ] Failure modes are documented
[ ] Evaluation data exists
[ ] Observability is designed
[ ] Rollback/change strategy exists
```
