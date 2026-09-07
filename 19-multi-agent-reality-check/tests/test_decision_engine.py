from app.decision_engine import Architecture, Requirements, recommend, score_architectures, should_upgrade_to_multi_agent


def test_scores_are_bounded():
    scores = score_architectures(Requirements(parallelism=1, specialization=1, decomposition=1, contractability=1))
    assert all(0 <= value <= 1 for value in scores.values())


def test_multi_agent_can_win_for_parallel_specialized_work():
    r = Requirements(
        parallelism=1, specialization=1, decomposition=1, contractability=1,
        verification=0.9, latency_sensitivity=0.1, cost_sensitivity=0.1,
        coordination_risk=0.1, security_sensitivity=0.1,
    )
    assert recommend(r) == Architecture.MULTI_AGENT


def test_evidence_gate_rejects_expensive_non_improvement():
    assert not should_upgrade_to_multi_agent(
        baseline_success=0.80, multi_success=0.82,
        baseline_cost=1, multi_cost=3,
        baseline_latency=1, multi_latency=3,
    )


def test_evidence_gate_accepts_material_improvement():
    assert should_upgrade_to_multi_agent(
        baseline_success=0.80, multi_success=0.90,
        baseline_cost=1, multi_cost=1.5,
        baseline_latency=1, multi_latency=1.4,
    )
