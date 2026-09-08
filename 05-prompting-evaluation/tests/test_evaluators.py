from app.evaluators import exact_match, normalized_text_match, schema_check


def test_exact_match_is_deterministic():
    assert exact_match("Paris", "Paris") == 1.0
    assert exact_match("Paris", "London") == 0.0


def test_normalized_text_match_ignores_case_and_whitespace():
    assert normalized_text_match("Paris", "  PARIS  ") == 1.0
    assert normalized_text_match("Paris", "London") == 0.0


def test_schema_check_requires_all_keys():
    assert schema_check({"answer": "ok", "evidence": []}, ("answer", "evidence")) == 1.0
    assert schema_check({"answer": "ok"}, ("answer", "evidence")) == 0.0
