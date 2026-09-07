from __future__ import annotations
from dataclasses import dataclass, field
from time import perf_counter

@dataclass
class Trace:
    run_id: str
    spans: list[dict] = field(default_factory=list)

    def record(self, stage: str, **data):
        self.spans.append({"stage": stage, **data})

    def first_failure(self):
        for span in self.spans:
            if span.get("status") == "error":
                return span
        return None


def timed(trace: Trace, stage: str, fn, **meta):
    start = perf_counter()
    try:
        result = fn()
        trace.record(stage, status="ok", latency_ms=(perf_counter()-start)*1000, **meta)
        return result
    except Exception as exc:
        trace.record(stage, status="error", error_type=type(exc).__name__, error=str(exc), latency_ms=(perf_counter()-start)*1000, **meta)
        raise


def classify(trace: Trace) -> str:
    failure = trace.first_failure()
    if not failure:
        return "no_observed_failure"
    stage = failure["stage"]
    mapping = {
        "query": "query_transformation_failure",
        "retrieval": "candidate_generation_failure",
        "filter": "authorization_or_metadata_failure",
        "ranking": "ranking_failure",
        "evidence": "evidence_assembly_failure",
        "generation": "generation_failure",
    }
    return mapping.get(stage, "system_failure")
