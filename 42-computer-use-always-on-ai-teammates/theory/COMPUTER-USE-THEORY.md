# Module 42 — Computer Use & Always-On Teammates: Theory

## Mental model
A computer-use agent operates over partially observed state. The UI can change between observation and action, so every consequential action needs preconditions and postconditions. Structured APIs remain preferable when available.

## Observation stack
Screenshot gives pixels; DOM gives structure; accessibility trees give semantic controls; application APIs provide authoritative structured state. Teach confidence and disagreement between these views.

## Action contract
Every UI action should identify target, action type, expected precondition, scope, risk, timeout, approval requirement and expected postcondition. Re-observe after navigation, asynchronous updates or focus changes.

## Security boundary
Webpage/application text is untrusted data. It cannot redefine policy, credentials, tenant, approval or termination. Credentials should be brokered and never exposed unnecessarily to the model.

## Always-on architecture
`TRIGGER → TASK CONTRACT → POLICY → OBSERVE → ACT → VERIFY → CHECKPOINT → WAIT/RESUME`.

## Critical races
Stale UI, double-submit, session expiry, approval expiry, wrong-account context, browser popup hijacking and scheduled-trigger duplication.

## Invariants
1. No action against stale state when freshness is required.
2. Approval binds to exact consequential action and expires.
3. Credentials remain outside ordinary model context.
4. Data transfer crosses DLP controls.
5. Emergency shutdown prevents further autonomous actions.

## Exercises
Build a synthetic CRM worker; compare API-first and UI-first strategies; inject webpage prompt injection; force session expiry; submit a form twice; verify postconditions; calculate UI actions and cost per successful task.
