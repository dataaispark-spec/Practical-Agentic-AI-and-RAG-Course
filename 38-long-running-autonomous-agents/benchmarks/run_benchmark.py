"""Small deterministic benchmark for the M38 reference worker."""
from __future__ import annotations

import time
from app.worker import DurableJob, DurableWorker


def run() -> dict[str, float]:
    calls: list[str] = []

    def effect(effect_id: str) -> str:
        calls.append(effect_id)
        return f"applied:{effect_id}"

    worker = DurableWorker(effect)
    job = DurableJob("benchmark-001", "reconcile", total_steps=100)
    started = time.perf_counter()
    worker.run(job, steps=100, crash_after_effect_at=49)
    job.status = job.status.CREATED
    worker.run(job, steps=100)
    elapsed = time.perf_counter() - started

    unique = len(set(calls))
    return {
        "effects_attempted": float(len(calls)),
        "unique_effects": float(unique),
        "duplicate_effects": float(len(calls) - unique),
        "recovery_success": float(job.status == job.status.COMPLETED),
        "elapsed_seconds": elapsed,
    }


if __name__ == "__main__":
    print(run())
