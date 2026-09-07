from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class EvaluationCase:
    case_id: str
    input: str
    expected: str


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    passed: bool
    failure_category: str | None = None


def exact_match(expected: str, actual: str) -> bool:
    return expected.strip() == actual.strip()


def evaluate(cases: list[EvaluationCase], runner: Callable[[str], str]) -> list[CaseResult]:
    results: list[CaseResult] = []
    for case in cases:
        actual = runner(case.input)
        if exact_match(case.expected, actual):
            results.append(CaseResult(case.case_id, True))
        else:
            results.append(CaseResult(case.case_id, False, "incorrect_output"))
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
        "failure_categories": failures,
    }
