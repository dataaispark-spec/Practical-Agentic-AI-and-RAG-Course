# Enterprise IT Lab — Durable Change-Management Worker

## Scenario
Process change requests from intake through approval, implementation and verification.

## Build
Use durable CAB waiting, action-hash approval, role revalidation, tenant/object scope checks, effect ledger, DLQ and audit reconstruction.

## Failure injections
Duplicate ticket, requester role change, approval replay, implementation timeout and worker takeover.

## Required proof
An approval is valid only for the exact action and current authorization policy. Replayed events cannot create duplicate changes.
