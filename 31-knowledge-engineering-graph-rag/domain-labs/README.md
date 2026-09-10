# Module 31 — Domain Lab Pack

## Cybersecurity
Graph: `Asset → Vulnerability → Control → Owner`. Build a multi-hop SOC question set. Reject unsupported edges and preserve advisory evidence.

## Banking
Graph: `Customer → Account → Transaction → Case → Policy`. Enforce customer/tenant scope and produce evidence paths for investigations.

## Healthcare
Graph: `Patient → Encounter → Medication → Diagnosis → Guideline`. Separate clinical source evidence from generated explanations and apply privacy scope.

## Manufacturing
Graph: `Machine → Component → FailureMode → WorkOrder → Technician`. Find indirect maintenance dependencies.

## Enterprise IT
Graph: `Service → Dependency → Incident → Team → Runbook`. Reconstruct an outage path and cite every relationship.

## Assessment
For each domain: 20 labeled questions, 5 adversarial questions, one poisoned-edge test, one tenant-isolation test and one multi-hop benchmark. Report Recall@K, MRR, path accuracy, provenance coverage and latency.