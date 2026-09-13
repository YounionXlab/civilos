from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .report import generate_report
from .run import ExperimentRun, create_run, step_run


@dataclass(frozen=True)
class ScenarioDefinition:
    name: str
    initial_overrides: dict[str, float | int]
    shocks: dict[int, dict[str, float]]


SCENARIOS: dict[str, ScenarioDefinition] = {
    "baseline": ScenarioDefinition("baseline", {}, {}),
    "resource-stress": ScenarioDefinition(
        "resource-stress",
        {"energy": 45, "water": 45, "food": 50},
        {},
    ),
    "shock-stress": ScenarioDefinition(
        "shock-stress",
        {},
        {
            60: {"energy": -30},
            120: {"water": -30},
            180: {"food": -30},
            240: {"energy": -20, "water": -20, "food": -20},
        },
    ),
    "low-coordination": ScenarioDefinition(
        "low-coordination",
        {"cq": 0.15},
        {},
    ),
}


def _apply_shock(run: ExperimentRun, sol: int, delta: dict[str, float]) -> None:
    before = {key: run.world.get(key, 0) for key in delta}
    for key, value in delta.items():
        run.world[key] = round(max(0, min(100, float(run.world.get(key, 0)) + value)), 2)
    after = {key: run.world.get(key, 0) for key in delta}
    run.events.append(
        {
            "day": sol,
            "title": f"Runtime intervention at Sol {sol}",
            "description": "Deterministic comparative-scenario shock applied before the normal simulation tick.",
            "event_impact": dict(delta),
            "before": before,
            "after": after,
            "runtime_intervention": True,
        }
    )


def run_scenario(name: str) -> ExperimentRun:
    if name not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {name}")
    scenario = SCENARIOS[name]
    run = create_run()
    run.experiment = dict(run.experiment)
    run.experiment["scenario_label"] = scenario.name
    for key, value in scenario.initial_overrides.items():
        run.world[key] = value

    while run.status != "completed":
        next_sol = run.current_sol + 1
        if next_sol in scenario.shocks:
            _apply_shock(run, next_sol, scenario.shocks[next_sol])
        step_run(run)
    return run


def _recovery_summary(run: ExperimentRun) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for resource in ("energy", "water", "food"):
        values = [float(getattr(obs, resource)) for obs in run.observations]
        minimum = min(values)
        min_index = values.index(minimum)
        recovered_to_70 = next(
            (index + 1 for index, value in enumerate(values[min_index:], start=min_index) if value >= 70),
            None,
        )
        summary[resource] = {
            "minimum": minimum,
            "minimum_sol": min_index + 1,
            "recovered_to_70_sol": recovered_to_70,
        }
    return summary


def run_comparative_suite() -> dict[str, Any]:
    runs = {name: run_scenario(name) for name in SCENARIOS}
    reports = {name: generate_report(run).to_dict() for name, run in runs.items()}
    baseline_final = reports["baseline"]["final_state"]

    comparison: dict[str, Any] = {
        "experiment_id": runs["baseline"].experiment_id,
        "observation_window": runs["baseline"].observation_window,
        "scenarios": {},
    }
    for name, run in runs.items():
        report = reports[name]
        final_state = report["final_state"]
        comparison["scenarios"][name] = {
            "observations": len(run.observations),
            "final_state": final_state,
            "minimums": {key: report["metrics"][key]["min"] for key in ("energy", "water", "food", "cq")},
            "recovery": _recovery_summary(run),
            "result": report["result"],
            "delta_vs_baseline": {
                key: round(float(final_state[key]) - float(baseline_final[key]), 4)
                for key in baseline_final
            },
            "runtime_interventions": [
                event for event in run.events if event.get("runtime_intervention")
            ],
        }

    return {
        "reports": reports,
        "comparison": comparison,
    }
