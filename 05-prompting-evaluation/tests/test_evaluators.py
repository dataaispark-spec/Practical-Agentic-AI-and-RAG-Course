from app.evaluators import evaluate_exact_match, evaluate_contains


def test_exact_match_is_deterministic():
    assert evaluate_exact_match("Paris", "Paris") == 1.0
    assert evaluate_exact_match("Paris", "London") == 0.0


def test_contains_handles_grounded_answer():
    assert evaluate_contains("Paris is the capital of France", "Paris") == 1.0
    assert evaluate_contains("London is the capital", "Paris") == 0.0
