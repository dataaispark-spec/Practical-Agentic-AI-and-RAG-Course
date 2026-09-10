# Module 33 — Construction Benchmark

Compare rule-based, NER/model and structured-LLM extraction on the same labels.

Report entity precision/recall/F1, relation precision/recall/F1, unsupported-claim rate, provenance coverage, false merge rate, promotion precision, quarantine rate, duplicate-write rate, rollback success and downstream retrieval gain.

Release gate: aggregate accuracy is not enough; block releases on catastrophic false merges, tenant violations or unsupported high-risk promotions.