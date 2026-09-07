"""Lightweight structural QA checker for the 38-module Agentic AI + RAG course.

Run from repository root:
    python 00-course-roadmap/course_qa_checker.py

Use --strict when the course is expected to be fully compliant. The default mode
reports gaps without failing, because the repository is intentionally being upgraded
incrementally. This checker does not claim that notebooks executed successfully.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

KEYWORDS = {
    "theory": ["theory", "concept", "mental model", "mechanism"],
    "diagram": ["diagram", "architecture", "data flow", "control flow"],
    "industry": ["industry", "banking", "healthcare", "cybersecurity", "manufacturing", "enterprise", "e-commerce", "legal"],
    "failure": ["failure", "break", "fault", "injection", "debug"],
    "metrics": ["metric", "latency", "cost", "Recall@K", "success rate", "evaluation"],
    "security": ["security", "authorization", "tenant", "injection", "audit"],
    "challenge": ["challenge", "exercise", "mastery"],
    "solution": ["solution", "reference", "hint"],
    "interview": ["interview", "system design"],
}

REQUIRED_NOTEBOOK_SIGNALS = {
    "objectives": ["objective", "learning goals"],
    "concept_map": ["concept map"],
    "mechanism": ["mechanism", "first principles"],
    "build": ["BUILD", "guided"],
    "try": ["TRY", "TODO", "exercise"],
    "break": ["BREAK", "failure", "broken"],
    "measure": ["measure", "metric", "evaluation"],
    "security": ["security", "misuse", "attack"],
    "challenge": ["challenge", "mastery"],
    "solution": ["solution", "reference"],
}


def module_dir(number: int) -> Path | None:
    matches = sorted(ROOT.glob(f"{number:02d}-*"))
    return matches[0] if matches else None


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def notebook_text(path: Path) -> str:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    parts: list[str] = []
    for cell in data.get("cells", []):
        src = cell.get("source", [])
        parts.append("".join(src) if isinstance(src, list) else str(src))
    return "\n".join(parts)


def contains_any(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def score_module(number: int) -> dict:
    path = module_dir(number)
    if path is None:
        return {"module": number, "status": "MISSING", "score": 0, "missing": ["module directory"]}

    readme = read_text(path / "README.md")
    notebook_dir = path / "notebooks"
    notebooks = list(notebook_dir.glob("*.ipynb")) if notebook_dir.exists() else []
    nb_text = "\n".join(notebook_text(p) for p in notebooks)
    all_text = f"{readme}\n{nb_text}"

    evidence = {key: contains_any(all_text, terms) for key, terms in KEYWORDS.items()}
    nb_evidence = {key: contains_any(nb_text, terms) for key, terms in REQUIRED_NOTEBOOK_SIGNALS.items()}
    artifacts = {
        "readme": (path / "README.md").exists(),
        "notebook": bool(notebooks),
        "tests": bool(list(path.rglob("test_*.py"))),
        "app": (path / "app").exists(),
    }

    score = sum(evidence.values()) + sum(nb_evidence.values()) + sum(artifacts.values())
    missing = [k for k, v in evidence.items() if not v]
    missing += [f"notebook:{k}" for k, v in nb_evidence.items() if not v]
    missing += [k for k, v in artifacts.items() if not v]
    complete = all(evidence.values()) and all(nb_evidence.values()) and all(artifacts.values())
    return {
        "module": number,
        "status": "COMPLETE" if complete else "UPGRADE",
        "score": score,
        "missing": missing,
        "notebooks": [p.relative_to(ROOT).as_posix() for p in notebooks],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="fail unless all modules satisfy the structural contract")
    args = parser.parse_args()
    results = [score_module(i) for i in range(1, 39)]
    print("Agentic AI + RAG Course — structural QA")
    print("=" * 48)
    complete = 0
    for r in results:
        print(f"M{r['module']:02d}: {r['status']:<8} score={r['score']:02d}")
        if r["status"] == "COMPLETE":
            complete += 1
        if r["missing"]:
            print("  gaps:", ", ".join(r["missing"][:8]))
    print("=" * 48)
    print(f"Complete: {complete}/38")
    print("Note: repository-structure QA only; notebook execution requires a runtime pass.")
    return 0 if (complete == 38 or not args.strict) else 1


if __name__ == "__main__":
    raise SystemExit(main())
