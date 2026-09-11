# Cybersecurity Lab — Persistent SOC Investigation

## Scenario
Investigate a high-severity alert across endpoint, identity and ticket systems for several hours. Some actions require analyst approval.

## Build
Persist evidence provenance, investigation position, tenant/asset scope, approval binding and policy version. Use event-driven wakeups for analyst decisions.

## Failure injections
Duplicate alert, poisoned checkpoint, stale policy, expired approval, provider outage and stale worker takeover.

## Required proof
A stale approval or stale policy can never authorize containment. Every conclusion traces back to evidence; every containment effect has a durable identity.
