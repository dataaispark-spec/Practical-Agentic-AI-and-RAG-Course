# M38 Architecture Diagram Pack

## Durable control plane

```text
                         ┌───────────────────────┐
                         │ Goal / Task Contract  │
                         └───────────┬───────────┘
                                     ↓
                         ┌───────────────────────┐
                         │ Durable State Store   │◄──── policy/approval version
                         └───────────┬───────────┘
                                     ↓
       ┌────────────── Queue ────────┴──────────────┐
       ↓                                             ↓
┌──────────────┐                              ┌──────────────┐
│ Worker A     │                              │ Worker B     │
│ lease/fence  │                              │ takeover     │
└──────┬───────┘                              └──────┬───────┘
       └──────────────────┬──────────────────────────┘
                          ↓
                 ┌──────────────────┐
                 │ Policy + Budget │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Action Gateway   │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Effect Ledger    │
                 └────────┬─────────┘
                          ↓
                    External API
                          ↓
                 Verify / Reconcile
                          ↓
             Checkpoint / Wait / Recover
```

## Critical invariants

1. Only the current fencing token can commit authoritative state.
2. Every protected side effect has a stable business effect identity.
3. Unknown outcomes are reconciled; they are not assumed to be failures.
4. Resume revalidates authority and policy.
5. Budgets are cumulative across attempts.
6. Waiting is durable and event-driven.
7. Terminal history is reconstructable.
