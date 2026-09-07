# Architecture Decision Engine Lab

## Objective

Build a small, explainable architecture recommender from requirements rather than framework preference.

## Run

```bash
cd 01-ai-systems-thinking/labs/architecture-decision-engine
python architecture_decider.py
pytest -q
```

The lab intentionally starts with deterministic Python logic. Later modules will replace parts of the decision process with richer evaluation and production telemetry.

## Student upgrades

1. Replace `ValueError` validation with Pydantic models.
2. Add latency and budget constraints to the requirement model.
3. Return a confidence/explanation structure.
4. Add a machine-readable architecture policy file.
5. Add regression cases from the industry exercises.
6. Add a CLI.
7. Add API exposure in Module 3.
8. Add evaluation metrics in Module 5.
