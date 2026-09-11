# Research Lab — Long-Horizon Evidence Collector

## Scenario
Collect evidence from heterogeneous sources over a long horizon and produce a verified conclusion.

## Build
Separate authoritative evidence, compact working memory and derived summaries. Persist provenance, source identifiers, contradiction records and recovery position.

## Failure injections
Source outage, contradictory evidence, malicious content, context overflow and stale checkpoint.

## Required proof
Context compaction cannot erase authoritative evidence. Contradictions remain explicit. A recovery run can reconstruct which sources supported each conclusion.
