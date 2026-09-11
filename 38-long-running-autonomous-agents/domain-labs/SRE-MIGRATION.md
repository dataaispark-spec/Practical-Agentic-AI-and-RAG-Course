# SRE Lab — Overnight Migration Worker

## Scenario
Migrate a synthetic fleet with prechecks, backup, change, validation and rollback under a fixed maintenance window.

## Build
Model each phase with preconditions/postconditions, effect identity, checkpoint, deadline, cancellation semantics and rollback classification.

## Failure injections
Crash after change, partial fleet failure, expired lease, dependency outage and cancellation during an uncertain operation.

## Required proof
Resume must not repeat completed changes. Failed validation must enter a bounded recovery path. Report RTO, rollback time, backlog and SLO impact.
