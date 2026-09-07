from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class EvaluationCase:
    case_id: str
    input: str
    expected: Any
    metadata: dict[str, Any] | None = None


@dataclass(frozen=True)
class ModelOutput:
    value: Any
    latency_ms: float = 0.0
    cost_usd: float = 0.0
    metadata: dict[str, Any] | None = None


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    passed: bool
    score: float
    failure_category: str | None = None
    latency_ms: float = 0.0
    cost_usd: float = 0.0


def exact_match(expected: Any, actual: Any) -> float:
    return 1.0 if expected == actual else 0.0


def normalized_text_match(expected: str, actual: str) -> float:
    normalize = lambda value: " ".join(value.strip().lower().split())
    return 1.0 if normalize(expected) == normalize(actual) else 0.0


def schema_check(actual: Any, required_keys: tuple[str, ...]) -> float:
    if not isinstance(actual, dict):
        return 0.0
    return 1.0 if all(key in actual for key in required_keys) else 0.0


def classify_failure(case: EvaluationCase, output: ModelOutput) -> str | None:
    if output.value is None:
        return "missing_output"
    if isinstance(case.expected, dict) and not isinstance(output.value, dict):
        return "wrong_format"
    metadata = output.metadata or {}
    if (case.metadata or {}).get("requires_evidence") and not metadata.get("evidence"):
        return "missing_evidence"
    return "incorrect_output"


def evaluate(cases: list[EvaluationCase], runner: Callable[[str], ModelOutput | Any]) -> list[CaseResult]:
    results: list[CaseResult] = []
    for case in cases:
        raw = runner(case.input)
        output = raw if isinstance(raw, ModelOutput) else ModelOutput(raw)
        score = exact_match(case.expected, output.value)
        results.append(CaseResult(case.case_id, score == 1.0, score, None if score == 1.0 else classify_failure(case, output), output.latency_ms, output.cost_usd))
    return results


def summary(results: list[CaseResult]) -> dict[str, object]:
    total = len(results)
    passed = sum(r.passed for r in results)
    failures: dict[str, int] = {}
    for result in results:
        if result.failure_category:
            failures[result.failure_category] = failures.get(result.failure_category, 0) + 1
    return {
        "cases": total,
        "passed": passed,
        "task_success_rate": passed / total if total else 0.0,
        "mean_latency_ms": sum(r.latency_ms for r in results) / total if total else 0.0,
        "estimated_cost_usd": sum(r.cost_usd for r in results),
        "failure_categories": failures,
    }
