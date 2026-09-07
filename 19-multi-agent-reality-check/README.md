# Module 19 — Multi-Agent Reality Check

## Mission

Learn when multiple agents are actually justified—and when they are expensive theater.

The central engineering question is not **"Can we use multiple agents?"**. It is **"What measurable property of the problem improves enough to justify additional agents, coordination, latency, cost and failure surface?"**

## Learning outcomes

By the end of this module you can:

1. Decompose a task into independent, dependent, adversarial and sequential work.
2. Compare a single agent, deterministic workflow and multi-agent architecture on the same benchmark.
3. Model coordination overhead, token cost, latency and failure probability.
4. Select patterns using evidence rather than novelty.
5. Identify when parallel agents help and when they amplify errors.
6. Design explicit contracts between agents.
7. Prevent agent-to-agent privilege escalation.
8. Evaluate consensus, debate and specialist architectures.
9. Debug coordination failures.
10. Defend an architecture decision in a system-design interview.

## 1. The single-agent baseline

Always build the simplest credible baseline first:

`Task → One Agent → Tools → Verification`

Measure task success, latency, cost, tool calls, recovery rate and security incidents.

Then compare:

`Task → Planner → Workers → Aggregator → Verifier`

If the second architecture does not produce a meaningful improvement on the target workload, keep the single-agent design.

## 2. Why multi-agent systems are hard

Each additional agent introduces:

- another probabilistic decision-maker;
- communication tokens;
- serialization/deserialization boundaries;
- coordination failures;
- inconsistent state;
- duplicated retrieval;
- security identities;
- timeout/retry behavior;
- observability complexity;
- potentially multiplied cost.

A five-agent system is not automatically five times smarter. It can simply be five opportunities to misunderstand the task.

## 3. Taxonomy

| Pattern | Good fit | Main risk |
|---|---|---|
| Single agent | bounded tool task | context overload |
| Sequential specialists | dependent expertise | latency accumulation |
| Parallel workers | independent subtasks | duplicated work |
| Supervisor/worker | dynamic decomposition | supervisor bottleneck |
| Debate/critique | ambiguous reasoning | correlated errors |
| Hierarchical | large structured task | coordination complexity |
| Competitive agents | search/exploration | cost explosion |
| Pipeline | stable stages | brittle interfaces |
| Swarm | highly dynamic work | hard-to-debug behavior |

## 4. Decomposition test

Before adding an agent, ask:

1. Can the work be independently parallelized?
2. Does each specialist have materially different tools or context?
3. Can outputs be represented by a stable contract?
4. Can the aggregator verify the outputs?
5. Does specialization improve benchmark performance?
6. Is the coordination cost acceptable?
7. Does isolation improve security or reliability?
8. Can failures be contained to one worker?

If most answers are no, prefer a single agent or deterministic workflow.

## 5. Multi-dimensional decision score

For each architecture estimate:

`Utility = SuccessGain − CostPenalty − LatencyPenalty − CoordinationRisk − SecurityRisk`

This is not a universal mathematical truth; it is a decision framework that forces explicit assumptions.

Track:

- task success;
- quality by slice;
- p50/p95 latency;
- token/tool cost;
- coordination messages;
- duplicate work;
- failure propagation;
- recovery time;
- security violations.

## 6. Agent contracts

Every worker should have an explicit contract:

```text
Input schema
Allowed tools
Allowed resources
Expected output schema
Deadline
Budget
Failure semantics
Verification criteria
Escalation behavior
```

Do not let worker A silently grant worker B permissions.

## 7. Identity model

Each agent should have a principal/capability identity where practical:

`human → orchestrator → specialist → tool`

A downstream worker receives only the minimum delegated capability required for its task.

This directly connects to Module 18 security.

## 8. Coordination protocols

Useful deterministic protocols include:

- request/response;
- task queue;
- fan-out/fan-in;
- publish/subscribe;
- supervisor routing;
- explicit handoff;
- lease/claim;
- quorum/consensus;
- checkpointed workflow.

Prefer explicit messages over hidden shared state.

## 9. Consensus is not truth

Three agents agreeing does not prove correctness if they share:

- the same flawed retrieval;
- the same model bias;
- the same poisoned context;
- the same incorrect assumption.

Consensus is evidence only when agents have sufficiently independent failure modes and an independent verifier exists.

## 10. Detailed labs

### Lab 1 — Single vs multi-agent benchmark
Build one agent that answers an enterprise question. Then build three specialists plus an aggregator. Run the same golden dataset.

Measure quality, cost and latency. Keep the multi-agent version only if the improvement survives the benchmark.

### Lab 2 — Parallel decomposition
Split a research task into independent sources. Compare sequential and parallel execution. Add a global deadline.

### Lab 3 — Specialist routing
Create finance, legal and technical specialists. Route tasks using deterministic metadata plus model classification. Test ambiguous requests.

### Lab 4 — Supervisor failure
Inject a bad supervisor decision. Demonstrate how one routing error can corrupt an entire workflow. Add validation and fallback.

### Lab 5 — Contract violation
Make a worker return malformed output. The aggregator must reject it rather than infer missing fields silently.

### Lab 6 — Correlated-agent failure
Give every worker the same poisoned context. Show that majority voting can still fail. Add an independent verifier.

### Lab 7 — Cost explosion
Allow recursive delegation. Add maximum depth, total calls, tokens and cost budgets.

### Lab 8 — Security boundary
Attempt to make a low-privilege research worker call a high-impact finance tool. Prove Module 18 policy prevents the escalation.

### Lab 9 — Partial failure
Kill one worker during a fan-out. Recover only the failed branch without duplicating completed work.

### Lab 10 — Architecture decision engine
Implement a scorer that recommends deterministic workflow, single agent or multi-agent architecture based on measurable requirements.

## 11. Failure-first exercises

Break the system deliberately:

1. Remove worker output validation.
2. Remove delegation limits.
3. Give every agent identical broad permissions.
4. Remove correlation IDs.
5. Remove per-worker budgets.
6. Allow one worker to mutate another worker's state.
7. Make retries non-idempotent.
8. Let the supervisor invent tool permissions.
9. Remove independent verification.
10. Allow fan-out to continue after the global deadline.

For each failure document **trigger → blast radius → root cause → containment → regression test**.

## 12. Production architecture

```text
                  +----------------+
                  | Task Contract  |
                  +-------+--------+
                          |
                  +-------v--------+
                  | Orchestrator   |
                  | plan + budget  |
                  +---+---+---+----+
                      |   |   |
                 +----v+ +v---v----+ 
                 | W1 | | W2 | W3 |
                 +--+-+ +--+-+--+-+
                    |      |    |
                    +------+----+
                           v
                    +------+------+
                    | Aggregator  |
                    +------+------+
                           v
                    +------+------+
                    | Independent |
                    | Verifier    |
                    +-------------+
```

Every boundary should expose metrics and enforce identity/capabilities.

## 13. Observability

A multi-agent trace should reconstruct:

`run → task → agent → message → tool → result → verification`

Use correlation IDs and parent/child spans. Record prompt/version identifiers without leaking secrets.

## 14. Evaluation matrix

Create an experiment table with architecture × model × task slice × budget. Report confidence intervals where feasible. Include adversarial cases and partial failures.

Never compare architectures using different datasets or hidden budgets.

## 15. Industry scenarios

**Banking:** fraud analysis may parallelize independent evidence gathering, but payment execution should remain tightly authorized.

**Healthcare:** specialist agents may summarize different evidence sources, while final clinical workflows require independent verification and human governance.

**Cybersecurity:** reconnaissance can fan out; destructive remediation should remain capability-gated and approval-controlled.

**Enterprise IT:** ticket triage, knowledge retrieval and diagnostics may be specialized, while production mutation stays behind deterministic policy.

## 16. Interview questions

1. When is multi-agent architecture justified?
2. What is the strongest single-agent baseline?
3. Why can consensus fail?
4. How do you measure coordination overhead?
5. How do agents share state safely?
6. How do you prevent privilege escalation between agents?
7. How do you recover one failed worker?
8. What belongs in a worker contract?
9. How do you stop recursive delegation?
10. How do you evaluate multi-agent systems fairly?
11. When is a workflow better than an agent swarm?
12. What is the supervisor bottleneck?
13. How would you debug a wrong final answer when five agents participated?
14. How do you control cost?
15. How would you design multi-agent observability?

## 17. System-design challenge

Design an enterprise research platform that can search internal documents, public sources and structured databases, then produce an evidence-backed report.

Defend whether it should use one agent, parallel specialists or a hybrid deterministic workflow. Include contracts, identity, budgets, verification, failure recovery and security.

## 18. Coding challenges

- Implement fan-out/fan-in with bounded concurrency.
- Implement worker capability contracts.
- Implement per-agent and global budgets.
- Implement delegation depth limits.
- Implement correlation IDs.
- Implement partial-failure recovery.
- Implement architecture scoring.
- Implement independent verification.

## 19. Mastery gate

You pass when you can:

- build a single-agent baseline;
- build a comparable multi-agent variant;
- benchmark both fairly;
- quantify coordination overhead;
- isolate worker permissions;
- recover partial failure;
- demonstrate a case where multi-agent loses;
- demonstrate a case where specialization wins;
- defend the final architecture with evidence.

## Gold challenge

Build the **AegisAI Architecture Decision Engine**: given task characteristics, security constraints, latency/cost budgets and benchmark history, recommend deterministic workflow, single agent, or multi-agent architecture; then execute the selected architecture and emit a comparison report.

The winning architecture is not the one with the most agents. It is the one with the best measured outcome under the real constraints.
