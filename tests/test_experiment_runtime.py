from pathlib import Path

from packages.engine.experiments import (
    create_run,
    generate_report,
    load_experiment,
    run_experiment,
    step_run,
)

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments" / "exp-001-ares-alpha.json"


def test_experiment_json_loads_and_validates():
    experiment = load_experiment(EXPERIMENT)
    assert experiment["id"] == "EXP-CIV-001"
    assert "EXP-001" in experiment["legacy_aliases"]
    assert experiment["observation_window"] == {"value": 365, "unit": "sol"}


def test_run_id_exists_and_one_tick_creates_one_observation():
    run = create_run(load_experiment(EXPERIMENT))
    assert run.run_id.startswith("RUN-")
    assert run.status == "created"
    observation = step_run(run)
    assert run.status == "running"
    assert len(run.observations) == 1
    assert observation.sol == 1
    assert observation.experiment_id == "EXP-CIV-001"


def test_365_sol_run_completes_and_generates_report():
    run = run_experiment(load_experiment(EXPERIMENT))
    assert run.status == "completed"
    assert len(run.observations) == 365
    assert run.observations[-1].sol == 365
    report = generate_report(run)
    assert report.experiment["id"] == "EXP-CIV-001"
    assert set(report.metrics) == {"population", "energy", "water", "food", "technology", "cq"}
    assert report.result in {"supported", "partially_supported", "not_supported", "inconclusive"}
    assert report.insight


def test_deterministic_rerun_produces_same_final_state_and_report():
    experiment = load_experiment(EXPERIMENT)
    first = run_experiment(experiment)
    second = run_experiment(experiment)

    assert first.run_id != second.run_id
    assert first.world == second.world
    assert first.agents == second.agents
    assert [observation.to_dict() | {"run_id": None} for observation in first.observations] == [
        observation.to_dict() | {"run_id": None} for observation in second.observations
    ]
    assert generate_report(first).to_dict() == generate_report(second).to_dict()
