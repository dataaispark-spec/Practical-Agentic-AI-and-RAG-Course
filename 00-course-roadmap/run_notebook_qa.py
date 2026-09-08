from __future__ import annotations

import argparse
import os
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = {
    1: "01-ai-systems-thinking",
    2: "02-python-ai-engineering",
    3: "03-fastapi-testing",
    6: "06-rag-from-first-principles",
    31: "31-knowledge-engineering-graph-rag",
    32: "32-graph-engineering-temporal-knowledge",
    33: "33-agentic-knowledge-graph-construction",
    34: "34-graph-vector-hybrid-retrieval",
    35: "35-compounding-knowledge-llm-wiki",
    36: "36-loop-engineering",
    37: "37-harness-engineering",
    38: "38-long-running-autonomous-agents",
    39: "39-skills-memory-continual-harnesses",
    40: "40-environments-verifiers-agentic-rl",
    41: "41-recursive-self-improving-agents",
    42: "42-computer-use-always-on-ai-teammates",
    43: "43-frontier-graph-rag-agentic-capstone",
}


def module_dir(n: int) -> Path:
    if n in CANONICAL:
        return ROOT / CANONICAL[n]
    matches = sorted(ROOT.glob(f"{n:02d}-*"))
    if not matches:
        raise FileNotFoundError(f"No canonical module directory found for M{n:02d}")
    return matches[0]


def notebooks(modules: list[int]):
    for n in modules:
        d = module_dir(n)
        notebook_dir = d / "notebooks"
        if not notebook_dir.exists():
            raise FileNotFoundError(f"M{n:02d}: missing notebooks directory: {notebook_dir}")
        files = sorted(notebook_dir.glob("*.ipynb"))
        if not files:
            raise FileNotFoundError(f"M{n:02d}: no .ipynb notebook found in {notebook_dir}")
        for p in files:
            yield n, p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modules", default="1-43")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--continue-on-error", action="store_true")
    args = ap.parse_args()

    start, end = map(int, args.modules.split("-"))
    if not (1 <= start <= end <= 43):
        ap.error("--modules must be an inclusive range within 1-43")

    os.environ.setdefault("MOCK_LLM", "true")
    os.environ.setdefault("OPENAI_API_KEY", "")
    os.environ.setdefault("ANTHROPIC_API_KEY", "")

    failures = []
    total = 0
    try:
        selected = list(notebooks(list(range(start, end + 1))))
    except Exception as exc:
        print(f"NOTEBOOK DISCOVERY FAILURE: {exc}")
        return 1

    for n, p in selected:
        total += 1
        print(f"EXECUTE M{n:02d}: {p.relative_to(ROOT)}")
        try:
            nb = nbformat.read(p, as_version=4)
            module_root = p.parent.parent
            existing = os.environ.get("PYTHONPATH", "")
            os.environ["PYTHONPATH"] = str(module_root) + (os.pathsep + existing if existing else "")
            NotebookClient(
                nb,
                timeout=args.timeout,
                kernel_name="python3",
                resources={"metadata": {"path": str(p.parent)}},
            ).execute()
            print(f"PASS M{n:02d}: {p.name}")
        except Exception as exc:
            failures.append((n, p, str(exc)))
            print(f"FAIL M{n:02d}: {p.name}: {exc}")
            if not args.continue_on_error:
                break

    print(f"Notebook QA: {total - len(failures)}/{total} passed")
    if failures:
        print("Failures:")
        for n, p, exc in failures:
            print(f"- M{n:02d} {p}: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
