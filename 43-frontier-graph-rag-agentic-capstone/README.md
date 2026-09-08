# Module 38 — Frontier Agentic RAG Capstone

## AegisAI — Autonomous Enterprise Intelligence Platform

## Mission

Build the complete production-style system that integrates the engineering ideas developed throughout the course:

```text
LLM
+ RAG
+ Retrieval
+ Tools
+ Agents
+ Loops
+ Harness
+ Memory
+ Skills
+ MCP
+ Multi-agent coordination
+ Long-running execution
+ Computer use
+ Environments
+ Verifiers
+ Evaluation
+ Cost controls
+ Security
+ Governance
+ CI/CD
+ Controlled self-improvement
```

This is not a chatbot capstone.

It is an **AI operating platform for bounded enterprise work**.

The central engineering model is:

```text
Agent
 = Model
 + Harness
 + Environment
 + Tools
 + State
 + Policy
 + Verification
 + Evaluation
```

The capstone must demonstrate that every component has a clear contract, measurable behavior and failure-recovery strategy.

---

# 1. Capstone objective

AegisAI accepts an enterprise goal such as:

> Investigate a customer issue, retrieve authoritative internal evidence, inspect permitted business systems, propose a resolution, request approval for consequential actions, execute the approved workflow and produce an auditable report.

The system should be able to:

1. understand the goal
2. classify the task and risk
3. retrieve trusted knowledge
4. plan bounded work
5. select tools
6. execute actions
7. maintain durable state
8. verify intermediate results
9. recover from failures
10. request human approval where required
11. complete the task
12. produce evidence and audit records
13. evaluate its own result
14. learn only through controlled, tested improvement

---

# 2. Reference architecture

```text
                              USER / EVENT
                                   |
                                   v
                           API / EVENT GATEWAY
                                   |
                                   v
                         TASK + RISK CLASSIFIER
                                   |
                 +-----------------+------------------+
                 |                                    |
                 v                                    v
          SIMPLE WORKFLOW                         AGENT RUN
                                                      |
                                                      v
                                              +---------------+
                                              |    HARNESS    |
                                              +---------------+
                                                      |
             +-------------------+--------------------+------------------+
             |                   |                    |                  |
             v                   v                    v                  v
          PLANNER             MEMORY              SKILLS             POLICY
             |                   |                    |                  |
             +-------------------+--------------------+------------------+
                                 |
                                 v
                          AGENT LOOP ENGINE
                                 |
          +----------------------+----------------------+
          |                      |                      |
          v                      v                      v
       RAG TOOLS             BUSINESS APIs        COMPUTER USE
          |                      |                      |
          v                      v                      v
    VECTOR / HYBRID          ENTERPRISE APPS       BROWSER / VM
    RETRIEVAL + RERANKER
          |                      |                      |
          +----------------------+----------------------+
                                 |
                                 v
                            VERIFICATION
                                 |
                      +----------+----------+
                      |                     |
                      v                     v
                   APPROVAL             RECOVERY
                      |                     |
                      +----------+----------+
                                 |
                                 v
                              RESULT
                                 |
               +-----------------+----------------+
               |                 |                |
               v                 v                v
           EVALUATION         AUDIT          ARTIFACTS
               |
               v
       IMPROVEMENT PIPELINE
               |
          SANDBOX + TESTS
               |
         CANARY / ROLLBACK
```

---

# 3. Architecture principles

## Principle 1 — Deterministic control around probabilistic decisions

The model can propose.

The system must validate.

```text
LLM proposal
    ↓
schema validation
    ↓
policy validation
    ↓
execution
    ↓
verification
```

## Principle 2 — Evidence before confidence

A confident answer is not necessarily a correct answer.

AegisAI should prefer:

```text
evidence → reasoning → answer
```

over:

```text
answer → search for supporting evidence
```

## Principle 3 — Verification is a first-class subsystem

Every consequential workflow needs an explicit success condition.

## Principle 4 — Authority is bounded

An agent should have only the permissions required for its current job.

## Principle 5 — Persistence increases responsibility

A durable worker can act later, so authorization, expiration, cancellation and audit must survive restarts.

## Principle 6 — Improvement is gated

A self-modifying system cannot promote its own changes solely because its own evaluator says they are better.

---

# 4. Task contract

Every task begins with a durable contract:

```yaml
task_id: unique-id
goal: business objective
owner: principal
tenant: tenant-id
risk_level: low|medium|high
time_budget: seconds
token_budget: integer
tool_budget: integer
action_budget: integer
allowed_systems: []
required_approvals: []
success_conditions: []
expiry: timestamp
```

The contract becomes the root of authorization, budgeting, evaluation and audit.

---

# 5. RAG subsystem

The RAG layer should support:

```text
ingestion
 → normalization
 → chunking
 → metadata
 → embeddings
 → vector index
 → lexical index
 → hybrid retrieval
 → filtering
 → reranking
 → context construction
 → citation/evidence tracking
```

Required metadata should include at least:

- document identity
- version
- source
- tenant
- timestamp
- access classification
- content hash
- lineage

Do not retrieve documents the agent is not authorized to read.

---

# 6. Retrieval quality gates

Measure:

```text
Recall@K
Precision@K
MRR / ranking quality
context relevance
answer faithfulness
citation correctness
```

Create an evaluation dataset with:

- normal questions
- ambiguous questions
- unanswerable questions
- stale-document questions
- conflicting-document questions
- authorization-sensitive questions

---

# 7. Agent loop

Use an explicit state machine:

```text
OBSERVE
   ↓
DECIDE
   ↓
ACT
   ↓
VERIFY
   ↓
  ├── success → STOP
  ├── recoverable failure → RECOVER
  ├── approval required → WAIT
  ├── budget exhausted → STOP
  └── no progress → ESCALATE
```

Never rely on a vague `while True` loop.

Every iteration should have:

- state
- action
- observation
- progress signal
- budget consumption
- verification result
- next transition

---

# 8. Harness

The AegisAI harness owns the execution environment.

Responsibilities:

```text
context management
state
memory
skills
tool registry
sub-agents
workspace
checkpoints
retries
approvals
budgets
policy
audit
telemetry
recovery
evaluation hooks
```

The harness must be replaceable independently from the underlying model.

That separation makes model upgrades safer.

---

# 9. Memory architecture

Use separate stores for different purposes:

```text
working state
     |
episodic history
     |
semantic memory
     |
user / tenant preferences
     |
procedural skills
     |
execution checkpoints
```

Memory must have:

- provenance
- retention policy
- tenant scope
- sensitivity classification
- deletion semantics
- retrieval policy

Do not allow arbitrary historical text to become permanent agent authority.

---

# 10. Skills

Skills are reusable procedural knowledge loaded when relevant.

A skill should specify:

```text
name
purpose
inputs
procedure
constraints
examples
verification
failure handling
version
owner
```

Use progressive disclosure rather than placing every skill into every prompt.

Skill changes should be tested like software changes.

---

# 11. Tool layer

Every tool requires a contract:

```text
name
input schema
output schema
authorization scope
side-effect class
timeout
retry policy
cost
rate limit
verification method
```

Classify tools:

```text
READ
WRITE
EXTERNAL_COMMUNICATION
FINANCIAL
DESTRUCTIVE
ADMINISTRATIVE
```

Higher-risk tools require stronger controls.

---

# 12. MCP boundary

Treat external tool protocols as an integration boundary rather than as implicit trust.

For every connected tool server record:

- owner
- endpoint identity
- available tools
- permissions
- data classification
- allowed tenants
- rate limits
- audit requirements

AegisAI should be able to disable an individual tool without disabling the entire platform.

---

# 13. Computer-use subsystem

Use computer interaction only when structured interfaces are insufficient.

```text
API
 ↓ if unavailable
native integration
 ↓ if unavailable
computer/browser environment
```

Computer-use actions require:

- observation
- precondition validation
- bounded action
- postcondition verification
- evidence capture

Treat webpage/application content as untrusted input.

---

# 14. Multi-agent strategy

The default should be **one agent**.

Introduce additional agents only when specialization or isolation produces measurable value.

Possible roles:

```text
Supervisor
Researcher
Retriever
Analyst
Executor
Verifier
Security reviewer
```

Every delegation requires:

- bounded task
- explicit input
- explicit output contract
- timeout
- budget
- authority scope

Avoid multi-agent systems whose only purpose is making the architecture look impressive.

---

# 15. Long-running execution

AegisAI must survive:

- process restart
- worker crash
- network failure
- tool timeout
- model timeout
- human approval delay
- credential/session expiry
- temporary service outage

Use:

```text
persistent run record
checkpoint
lease/heartbeat
retry
idempotency key
reconciliation
resume
cancel
```

A run must never depend on process memory alone.

---

# 16. Environment and verifier

Represent important tasks as environments:

```text
reset()
observe()
step(action)
is_terminal()
snapshot()
restore(snapshot)
```

Separate:

```text
task definition
from
environment implementation
from
verifier
```

A verifier determines whether the goal was actually achieved.

---

# 17. Verification ladder

Use the strongest practical verifier:

```text
Level 0 — model says success
Level 1 — schema/state check
Level 2 — deterministic business rule
Level 3 — independent source check
Level 4 — test suite / simulation
Level 5 — human verification
```

Do not use a weaker verifier merely because it is cheaper when the consequence of error is high.

---

# 18. Security architecture

Threat model:

```text
user
 ↓
agent
 ↓
tools
 ↓
enterprise systems
```

Potential attacks include:

- prompt injection
- malicious retrieved content
- poisoned documents
- tool abuse
- privilege escalation
- credential theft
- data exfiltration
- confused-deputy attacks
- cross-tenant leakage
- unsafe autonomous actions
- evaluator manipulation
- malicious skill updates

Controls:

```text
input validation
access control
least privilege
sandboxing
policy engine
DLP
approval gates
output validation
audit
rate limits
circuit breakers
kill switch
```

---

# 19. Observability

Every run should emit structured events:

```json
{
  "run_id": "...",
  "task_id": "...",
  "step": 12,
  "state": "VERIFY",
  "tool": "search_knowledge",
  "latency_ms": 420,
  "tokens": 1800,
  "cost": 0.02,
  "policy": "allow",
  "verification": "pass"
}
```

Never store raw secrets in telemetry.

Track traces across:

```text
request
 → retrieval
 → model call
 → tool call
 → approval
 → computer action
 → verification
```

---

# 20. Evaluation framework

Create separate test sets for:

### RAG

- retrieval
- grounding
- citations

### Agent

- task completion
- tool selection
- planning
- termination

### Safety

- policy violations
- prompt injection
- unauthorized access
- data leakage

### Production

- latency
- cost
- reliability
- recovery

### Frontier capabilities

- long-running completion
- durable recovery
- computer-use success
- self-improvement regression safety

---

# 21. Cost engineering

Compute cost at the business-outcome level:

```text
cost / successful task
```

not merely:

```text
cost / LLM call
```

Implement:

- model routing
- token budgets
- tool budgets
- action budgets
- caching
- retrieval limits
- early stopping
- cheaper verification where appropriate
- escalation to stronger models only when needed

---

# 22. Self-improvement pipeline

AegisAI may propose improvements but must not silently deploy them.

```text
baseline
   ↓
trajectory analysis
   ↓
improvement hypothesis
   ↓
candidate change
   ↓
sandbox
   ↓
regression suite
   ↓
security suite
   ↓
benchmark
   ↓
canary
   ↓
promote / reject / rollback
```

Track improvement provenance:

```text
baseline version
change
reason
training/evaluation data
metrics
verifier results
approver
promotion decision
```

---

# 23. Continuous evaluation

Every production change should be evaluated against a fixed regression suite.

Minimum scorecard:

| Dimension | Metric |
|---|---|
| RAG | Recall@K |
| Grounding | Faithfulness |
| Agent | Task success |
| Tools | Correct tool selection |
| Reliability | Recovery rate |
| Latency | p50 / p95 / p99 |
| Cost | Cost/task |
| Safety | Unsafe-action rate |
| Security | Injection-block rate |
| Computer use | Verified task success |
| Long-running | Resume success |
| Improvement | Regression delta |

---

# 24. Deployment architecture

```text
                    Load Balancer
                         |
                    API Gateway
                         |
                 Task / Auth Service
                         |
                 Durable Run Queue
                         |
          +--------------+--------------+
          |                             |
     Agent Workers                 Workflow Workers
          |                             |
          +--------------+--------------+
                         |
                    Tool Gateway
                         |
       +-----------------+------------------+
       |                 |                  |
      RAG              APIs            Computer VM
       |                 |                  |
       +-----------------+------------------+
                         |
                 Policy / Approval
                         |
                    Verification
                         |
              Evaluation / Observability
                         |
                Audit / Data Platform
```

Use isolated execution for computer-use and high-risk workloads.

---

# 25. CI/CD gates

Pull requests should run:

```text
unit tests
integration tests
RAG regression
agent trajectory tests
security tests
policy tests
prompt-injection tests
cost checks
latency checks
schema checks
```

Deployment stages:

```text
dev
 ↓
test
 ↓
sandbox
 ↓
canary
 ↓
production
```

Production promotion should require passing predefined gates.

---

# 26. Incident response

Create runbooks for:

- hallucination spike
- retrieval degradation
- model outage
- tool outage
- credential compromise
- prompt-injection campaign
- runaway agent
- cost explosion
- cross-tenant leakage
- unsafe action
- corrupted memory
- bad self-improvement release

Emergency controls:

```text
pause all agents
pause tenant
revoke tool
revoke credential
block action class
rollback version
quarantine memory/skill
```

---

# 27. Capstone implementation phases

## Phase 1 — Foundation

Build:

- repository structure
- configuration
- typed models
- logging
- testing
- task contract

## Phase 2 — RAG

Build:

- ingestion
- indexing
- hybrid retrieval
- reranking
- citations
- evaluation

## Phase 3 — Agent

Build:

- tool registry
- agent loop
- budgets
- termination
- verification

## Phase 4 — Harness

Build:

- durable state
- checkpoints
- memory
- skills
- policy

## Phase 5 — Enterprise actions

Build:

- approvals
- business APIs
- MCP integration
- audit

## Phase 6 — Computer use

Build:

- isolated browser/VM
- observation
- action validation
- verification
- recovery

## Phase 7 — Long-running workers

Build:

- queue
- scheduling
- leases
- heartbeats
- resume
- cancellation

## Phase 8 — Evaluation

Build:

- benchmark suite
- regression harness
- safety suite
- cost/latency dashboards

## Phase 9 — Controlled improvement

Build:

- trajectory store
- failure analysis
- candidate generation
- sandbox evaluation
- canary/rollback

## Phase 10 — Production

Build:

- CI/CD
- deployment
- observability
- security controls
- runbooks
- governance

---

# 28. Suggested enterprise scenarios

Implement at least three end-to-end scenarios.

### Scenario A — Customer operations

Retrieve customer policy → inspect account → draft response → approval → update record → verify → audit.

### Scenario B — IT operations

Investigate incident → retrieve runbook → inspect permitted systems → propose remediation → approval → execute → verify → produce incident report.

### Scenario C — Knowledge operations

Monitor incoming requests → retrieve authoritative documents → classify → answer or escalate → maintain evidence → evaluate response quality.

Use synthetic or authorized datasets for the capstone.

---

# 29. Failure injection program

The capstone is incomplete until it fails deliberately.

Inject:

```text
wrong retrieval
stale documents
duplicate documents
contradictory sources
model timeout
tool timeout
malformed tool output
infinite loop
no-progress loop
budget exhaustion
queue duplication
worker crash
stale checkpoint
expired approval
revoked credential
prompt injection
malicious webpage
cross-tenant access attempt
computer UI drift
bad verifier
cost explosion
self-improvement regression
```

For every failure document:

```text
symptom
root cause
detection
containment
recovery
prevention
regression test
```

---

# 30. Final engineering scorecard

AegisAI should report a single scorecard containing:

```text
Task Success
RAG Quality
Grounding
Tool Accuracy
Loop Efficiency
Recovery Rate
Approval Safety
Security
Computer-use Success
Long-running Reliability
Latency
Cost
Observability Coverage
Regression Safety
Improvement Quality
```

Do not collapse everything into one vanity score during development. Preserve the dimensions so tradeoffs remain visible.

---

# 31. Interview mastery bank

### Architecture

1. Design an enterprise Agentic RAG platform from scratch.
2. Where does the agent end and the harness begin?
3. Why is a durable agent different from a chatbot?
4. When should an agent become multi-agent?
5. Where should policy enforcement live?

### RAG

6. Design hybrid retrieval at enterprise scale.
7. Debug a sudden Recall@K regression.
8. Prevent unauthorized document retrieval.
9. Handle conflicting document versions.
10. Design citation verification.

### Agents

11. Design a bounded agent loop.
12. Prevent infinite reasoning/tool loops.
13. Design tool contracts.
14. Implement durable checkpoints.
15. Recover a worker after a crash.

### Security

16. Defend against indirect prompt injection.
17. Prevent confused-deputy behavior.
18. Design least-privilege agent identity.
19. Protect credentials from computer-use agents.
20. Design emergency shutdown.

### Production

21. Design for 10,000 concurrent agent runs.
22. Control token and tool costs.
23. Debug p95 latency spikes.
24. Design model failover.
25. Design auditability.

### Frontier

26. Explain loop engineering.
27. Explain harness engineering.
28. How do skills differ from memory?
29. How should an agent learn from trajectories safely?
30. What is the role of an environment and verifier in agentic RL?
31. How would you evaluate a self-improving agent?
32. How do always-on workers change authorization?
33. When is computer use justified?
34. How would you combine APIs and computer use?
35. How do you prevent an evaluator from being gamed?

---

# 32. Mastery gate

You pass the capstone only when you can demonstrate all of the following:

- [ ] RAG with measurable retrieval quality
- [ ] grounded responses with evidence
- [ ] typed tool contracts
- [ ] bounded agent loop
- [ ] explicit termination conditions
- [ ] durable state
- [ ] memory with provenance
- [ ] governed skills
- [ ] policy engine
- [ ] human approval
- [ ] MCP or equivalent integration boundary
- [ ] computer-use sandbox
- [ ] long-running worker
- [ ] environment abstraction
- [ ] independent verifier
- [ ] observability
- [ ] cost controls
- [ ] security tests
- [ ] prompt-injection defenses
- [ ] CI/CD regression gates
- [ ] failure-injection tests
- [ ] rollback mechanism
- [ ] controlled improvement pipeline
- [ ] complete audit trail
- [ ] emergency shutdown

---

# 33. Gold challenge

Build a complete autonomous enterprise workflow in which:

1. A task arrives asynchronously.
2. The system creates a durable task contract.
3. RAG retrieves authorized evidence.
4. The agent develops a bounded plan.
5. A tool is selected through a typed contract.
6. The tool returns an unexpected result.
7. The agent detects the failure and recovers.
8. The workflow requires computer use.
9. A webpage contains malicious instructions.
10. The agent treats those instructions as untrusted.
11. A consequential action requires approval.
12. The approval becomes stale because state changes.
13. The agent invalidates the approval.
14. The target is revalidated.
15. The action executes.
16. An independent verifier confirms the outcome.
17. The worker checkpoints and completes.
18. The system produces an auditable evidence package.
19. Evaluation scores the trajectory.
20. A proposed improvement is tested in a sandbox but cannot bypass regression/security gates.

This single challenge should exercise nearly every major concept in the course.

---

# 34. What you should be able to explain after this course

You should be able to defend the following statement in an engineering interview:

> **An enterprise agent is not an LLM wrapped in tools. It is a governed software system in which a probabilistic model operates inside a deterministic harness, bounded environment and explicit authorization model, with durable state, verification, evaluation, recovery and auditability.**

And you should be able to prove it with code.

---

# 35. Final deliverables

The capstone repository should contain:

```text
38-frontier-agentic-rag-capstone/
├── README.md
├── architecture/
├── adr/
├── app/
├── agents/
├── harness/
├── rag/
├── tools/
├── mcp/
├── memory/
├── skills/
├── computer_use/
├── environments/
├── verifiers/
├── evaluation/
├── security/
├── observability/
├── workflows/
├── tests/
├── failure-lab/
├── deployment/
├── runbooks/
└── docs/
```

The goal is not maximum code volume.

The goal is **engineering evidence**: every important design decision should be executable, testable, measurable and explainable.

---

# Course completion

Modules 1–30 establish the IITM-aligned engineering foundation.

Modules 31–37 extend it into frontier agent engineering:

```text
Loop
 → Harness
 → Long-running execution
 → Skills/Memory
 → Environments/Verifiers/RL
 → Self-improvement
 → Computer Use / Always-On Workers
```

Module 38 integrates the entire stack into AegisAI.

**You are now expected to think less like someone who merely calls an LLM API and more like an engineer designing an AI system that must survive contact with reality.**
