from packages.engine.experiments.scenarios import SCENARIOS, run_comparative_suite, run_scenario


def test_all_four_scenarios_complete_with_365_observations():
    for name in SCENARIOS:
        run = run_scenario(name)
        assert run.status == "completed"
        assert len(run.observations) == 365
        assert run.experiment_id == "EXP-CIV-001"


def test_scenarios_are_deterministic():
    first = run_comparative_suite()
    second = run_comparative_suite()
    assert first == second


def test_shock_stress_records_runtime_interventions():
    run = run_scenario("shock-stress")
    interventions = [event for event in run.events if event.get("runtime_intervention")]
    assert [event["day"] for event in interventions] == [60, 120, 180, 240]
    assert interventions[0]["event_impact"] == {"energy": -30}
    assert interventions[-1]["event_impact"] == {"energy": -20, "water": -20, "food": -20}


def test_stress_scenarios_materially_differ_from_baseline():
    suite = run_comparative_suite()["comparison"]["scenarios"]
    baseline = suite["baseline"]
    assert suite["resource-stress"]["minimums"] != baseline["minimums"]
    assert suite["shock-stress"]["minimums"] != baseline["minimums"]
    assert suite["low-coordination"]["minimums"]["cq"] < baseline["minimums"]["cq"]
