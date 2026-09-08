# Module 37 — Computer Use & Always-On AI Teammates

## Mission

Build an enterprise digital worker that can operate across browsers and applications, maintain durable work state, request approval at trust boundaries, and continue delegated work without requiring a human to drive every individual step.

This module moves the agent from:

```text
chat + API tools
```

toward:

```text
persistent identity
      +
computer/application environment
      +
visual interaction
      +
tools/APIs
      +
durable goals
      +
policy
      +
verification
      +
human approval
```

The objective is not to build an unrestricted autonomous bot. It is to understand the engineering controls required when an AI system can operate software on behalf of a person or organization.

---

# Learning outcomes

You will learn to:

- distinguish API agents from computer-use agents
- model browser/desktop interaction as an environment
- build an observation-action-verification loop for UI tasks
- handle screenshots, DOM/accessibility information and application state
- design persistent agent identity and authorization
- implement approval gates for high-impact actions
- make UI actions idempotent where possible
- detect stale screens and changed application state
- recover from navigation, timeout and UI failures
- design always-on workers with schedules and event triggers
- audit computer actions
- combine UI automation with deterministic APIs
- design enterprise-grade digital workers without granting excessive authority

---

# 1. Why computer use changes the problem

An API tool usually provides a structured contract:

```text
create_ticket(title, priority)
```

Computer use may instead require:

```text
observe screen
 ↓
locate application
 ↓
click
 ↓
type
 ↓
wait
 ↓
observe changed state
 ↓
verify
```

The second system operates in a partially observable, stateful environment.

Therefore UI automation requires stronger:

- state detection
- verification
- timeout handling
- permission boundaries
- recovery
- screenshot/evidence capture

---

# 2. Computer-use architecture

```text
                    GOAL
                     |
                     v
                Agent Loop
                     |
            +--------+--------+
            |                 |
        Observation         Policy
            |                 |
     +------+-------+         |
     |              |         |
  Screenshot       DOM/A11y   |
     |              |         |
     +------+-------+---------+
            |
            v
        Action Planner
            |
     +------+------+------+
     |             |      |
   Mouse         Keyboard API/tool
     |             |      |
     +------+------+------+
            |
            v
        Environment
            |
            v
       Verification
```

Use the richest reliable observation channel available. A DOM or accessibility tree can be more deterministic than relying exclusively on pixels.

---

# 3. Observation channels

Possible channels include:

### Pixels

Screenshots/video frames.

Strengths:

- works with almost any interface
- captures visual state

Weaknesses:

- ambiguous
- expensive to process
- sensitive to layout changes

### DOM

Structured browser page representation.

Strengths:

- precise selectors
- text/state information

Weaknesses:

- unavailable for some applications
- dynamic pages can change rapidly

### Accessibility tree

Semantic controls and labels.

Useful for:

- buttons
- fields
- roles
- keyboard navigation

### Application APIs

When available, prefer structured APIs for deterministic operations rather than imitating a human click path.

---

# 4. API-first, UI-second

A production digital worker should generally use:

```text
structured API
      ↓ if unavailable
application-native tool
      ↓ if unavailable
computer interaction
```

Why?

API calls normally provide better:

- schemas
- error handling
- observability
- idempotency
- performance

Computer use remains valuable for applications that lack usable APIs or require genuine end-user interaction.

---

# 5. Action contract

Never let the model emit arbitrary UI commands directly into the operating system.

Use a typed action layer:

```python
class Click:
    target: str
    expected_state: str

class TypeText:
    target: str
    text_ref: str

class Navigate:
    url: str
    expected_domain: str
```

Every action should have:

- target
- expected precondition
- allowed scope
- timeout
- verification condition
- sensitivity
- reversibility classification

---

# 6. Stale-state problem

Imagine the agent sees:

```text
"Approve payment"
```

It waits 20 seconds.

The page changes.

The same coordinates now mean:

```text
"Delete payment"
```

A blind coordinate click is unacceptable.

Require:

```text
observe
 ↓
validate expected state
 ↓
action
 ↓
verify resulting state
```

State should be revalidated before consequential actions.

---

# 7. High-impact action gates

Classify actions:

```text
LOW
  navigation
  search

MEDIUM
  create draft
  update non-critical record

HIGH
  send external communication
  purchase
  financial transfer
  delete data
  change production configuration
```

High-impact actions should require policy evaluation and, where appropriate, human approval.

```text
agent proposes
     ↓
policy
     ↓
approval required
     ↓
human decision
     ↓
execute
     ↓
verify
```

---

# 8. Persistent identity

An always-on agent needs more than a prompt.

Model:

```text
Agent Identity
├── owner
├── tenant
├── purpose
├── permissions
├── active sessions
├── credentials
├── schedules
├── memory namespace
└── audit identity
```

Never use a single unrestricted credential for all agents.

Use least privilege and short-lived credentials wherever practical.

---

# 9. Always-on lifecycle

```text
CREATED
  ↓
AUTHORIZED
  ↓
IDLE
  ↓
TRIGGERED
  ↓
RUNNING
  ↓
WAITING
  ├── APPROVAL
  ├── EVENT
  └── RETRY
  ↓
COMPLETED / FAILED / CANCELLED
```

A persistent agent should not continuously consume model calls while idle.

Use event-driven wakeups and scheduled execution.

---

# 10. Triggers

Possible triggers:

```text
schedule
email/event
webhook
calendar event
repository change
monitoring alert
human request
business workflow transition
```

Each trigger should be authenticated and authorized.

An incoming event is not automatically permission to perform every action associated with that event.

---

# 11. Human-in-the-loop design

Avoid approval spam.

Bad design:

```text
approve every click
```

Better:

```text
agent performs reversible low-risk steps
        ↓
reaches trust boundary
        ↓
request approval with evidence
        ↓
execute bounded action
        ↓
verify
```

Approval request should contain:

- intended action
- target
- reason
- expected impact
- evidence
- reversible/irreversible status
- expiry

---

# 12. Browser/application security

Computer-use agents face risks such as:

- malicious webpage content
- prompt injection in page text
- deceptive buttons
- credential exposure
- untrusted downloads
- data exfiltration
- cross-site navigation
- session hijacking

Treat page content as **untrusted input**.

Never let text displayed by a webpage redefine the agent's authority or system policy.

---

# 13. Data-loss prevention

Before transferring information:

```text
source data
   ↓
sensitivity classifier
   ↓
destination policy
   ↓
allow / redact / block / approve
```

Examples:

```text
customer PII → external website → block
public documentation → approved site → allow
financial report → external email → approval
```

---

# 14. Verification after UI actions

Never assume a click succeeded.

Use:

```text
action
 ↓
expected state
 ↓
observe
 ↓
verify
```

Examples:

```text
Submit form
 ↓
confirmation ID appears
```

```text
Send email
 ↓
message appears in Sent + server/API confirms
```

```text
Create record
 ↓
record ID exists and fields match
```

Cross-check critical actions using an independent source when practical.

---

# 15. Build project — AegisAI Digital Worker

Build a sandboxed enterprise worker capable of:

1. opening a business application
2. reading a work queue
3. researching relevant records
4. preparing a draft response
5. requesting approval
6. completing an approved action
7. recording evidence
8. returning to idle state

Components:

```text
IdentityManager
TriggerManager
ComputerController
BrowserController
ObservationManager
ActionValidator
PolicyEngine
ApprovalManager
Verifier
CredentialBroker
AuditStore
DurableRunStore
```

Required APIs:

```text
trigger(event)
start(run)
pause(run)
approve(action)
reject(action)
cancel(run)
inspect(run)
```

---

# 16. Hands-on experiment matrix

| Experiment | Change | Measure |
|---|---|---|
| Screenshot only | pixel observation | success |
| DOM-assisted | structured page state | success/latency |
| Accessibility-assisted | semantic controls | action accuracy |
| API-first | structured APIs | cost/reliability |
| UI-only | browser interaction | recovery rate |
| Approval gate | high-impact confirmation | unsafe-action rate |
| Persistent worker | scheduled triggers | completion rate |
| State revalidation | pre/post checks | stale-action rate |
| DLP | data-transfer policy | leakage prevention |

---

# 17. Failure laboratory

### Failure A — Coordinate drift

Change window layout and observe stale coordinate actions.

### Failure B — Page injection

Insert malicious instructions into page content.

The agent must ignore them as untrusted content.

### Failure C — Stale approval

Change the target after approval but before execution.

The approval should become invalid.

### Failure D — Duplicate action

Crash after a successful submission but before recording the result.

Use idempotency/reconciliation.

### Failure E — Credential leakage

Attempt to copy a secret into an external application.

DLP should block it.

### Failure F — Session expiry

Invalidate the browser session during execution.

The worker should recover safely rather than improvising credentials.

### Failure G — Always-on runaway

Create a trigger loop that repeatedly wakes the agent.

Verify rate limits and circuit breakers.

---

# 18. Metrics

Track:

```text
task_success_rate
action_success_rate
stale_action_rate
verification_failure_rate
human_approval_rate
unsafe_action_attempt_rate
credential_denial_rate
recovery_rate
mean_run_duration
cost_per_completed_task
trigger_loop_rate
```

Also track:

```text
UI actions / successful task
API actions / successful task
```

This helps determine whether computer use is actually necessary.

---

# 19. Production architecture

```text
                    Event Sources
                         |
                    Trigger Gateway
                         |
                  Durable Run Queue
                         |
                  Digital Worker
                         |
       +-----------------+----------------+
       |                 |                |
   Computer Use        APIs          Knowledge
       |                 |                |
       +-----------------+----------------+
                         |
                    Policy Engine
                         |
                 +-------+-------+
                 |               |
             Approval         Verifier
                 |               |
                 +-------+-------+
                         |
                     Audit Store
```

Keep the computer-use runtime isolated from core production credentials and data stores.

---

# 20. Cost and performance engineering

Computer interaction can be expensive because observations may involve screenshots, multimodal inference and multiple corrective actions.

Optimize by:

- using APIs where possible
- reducing screenshot frequency
- detecting unchanged state
- batching deterministic operations
- using structured selectors
- caching stable application state
- stopping when verification succeeds

Measure cost per successful business outcome, not merely cost per model call.

---

# 21. Enterprise governance

Define:

```text
who owns the agent?
what is its purpose?
what systems can it access?
what data can it read?
what actions can it perform?
which actions require approval?
when do permissions expire?
who can disable it?
what evidence is retained?
```

An always-on worker should have a clear operational owner and emergency disable mechanism.

---

# 22. Interview bank

### Conceptual

1. How is computer use different from API tool calling?
2. Why is UI state partially observable?
3. Why should APIs usually be preferred over UI automation?
4. What is stale-state risk?
5. What is an always-on agent?

### Engineering

6. How would you validate a click before executing it?
7. How do you recover from a changed UI?
8. How do you make UI actions idempotent?
9. How do you verify a consequential action?
10. How would you reduce computer-use cost?

### Security

11. How do you defend against webpage prompt injection?
12. How do you prevent credential exfiltration?
13. How do you implement least privilege?
14. How do you expire stale approvals?
15. How do you audit an agent operating a browser?

### System design

16. Design an always-on enterprise digital worker platform.
17. Design computer use for 100,000 concurrent agents.
18. Design approval infrastructure for financial actions.
19. Design browser-session isolation.
20. Design DLP for an autonomous enterprise worker.

---

# 23. System-design challenge

**Design an enterprise digital worker for customer operations.**

Constraints:

- multiple business applications
- browser + API integrations
- persistent schedules
- customer data
- external communications
- human approval for high-impact actions
- complete audit trail
- emergency shutdown
- 10,000 concurrent workers

Defend:

- identity model
- credential broker
- computer-use sandbox
- API/UI decision policy
- approval architecture
- verification
- DLP
- event triggers
- cost controls
- observability

---

# 24. Mastery gate

You pass when you can demonstrate:

1. A sandboxed computer-use environment.
2. Structured observations.
3. Typed actions.
4. Pre-action state validation.
5. Post-action verification.
6. Human approval at a trust boundary.
7. Persistent run state.
8. Crash recovery.
9. Prompt-injection resistance.
10. Credential/DLP protection.
11. Complete audit evidence.
12. Emergency shutdown.

## Gold challenge

Create a business workflow where the agent must navigate an application, encounter a malicious instruction embedded in the page, prepare a consequential action, request approval, detect that the page state changed after approval, invalidate the stale approval, revalidate the target and only then execute the safe action.

---

## Frontier connection

Modern persistent-agent products demonstrate that AI workers are moving beyond chat sessions toward durable identities, computer environments, application interaction, memory and autonomous work. The engineering lesson for this course is not "give the agent a computer and let it run."

It is:

```text
Persistent capability
        +
Persistent state
        +
Persistent authorization
        +
Persistent verification
        +
Persistent audit
```

The next module combines the entire course into the **Frontier Agentic RAG Capstone**: an enterprise platform with RAG, tools, agents, loops, harnesses, memory, environments, verifiers, computer use, governance and controlled self-improvement.
