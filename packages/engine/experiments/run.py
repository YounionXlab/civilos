from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from ..simulation import tick
from .loader import ROOT, load_experiment
from .observation import Observation, capture_observation


@dataclass
class ExperimentRun:
    run_id: str
    experiment: dict[str, Any]
    world: dict[str, Any]
    agents: list[dict[str, Any]]
    observations: list[Observation] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    status: str = "created"

    @property
    def experiment_id(self) -> str:
        return str(self.experiment["id"])

    @property
    def observation_window(self) -> int:
        return int(self.experiment["observation_window"]["value"])

    @property
    def current_sol(self) -> int:
        return len(self.observations)


def _load_seed_state(root: Path = ROOT) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    with (root / "data" / "world.json").open("r", encoding="utf-8") as handle:
        world = json.load(handle)
    with (root / "data" / "agents.json").open("r", encoding="utf-8") as handle:
        agents = json.load(handle)
    world["day"] = 0
    world["history"] = []
    world.pop("population_cooldown_until", None)
    return world, agents


def create_run(
    experiment: dict[str, Any] | None = None,
    *,
    root: Path = ROOT,
) -> ExperimentRun:
    definition = copy.deepcopy(experiment or load_experiment())
    world, agents = _load_seed_state(root)
    initial = definition["initial_conditions"]
    world["seed"] = definition.get("world_seed") or world.get("seed", "ARES-ALPHA-001")
    world["random_seed"] = definition.get("random_seed")
    world["population"] = int(initial.get("population", world.get("population", len(agents))))
    world["technology"] = float(initial.get("technology", world.get("technology", 0)))
    return ExperimentRun(
        run_id=f"RUN-{uuid4().hex}",
        experiment=definition,
        world=world,
        agents=agents,
    )


def step_run(run: ExperimentRun) -> Observation:
    if run.status == "completed":
        raise RuntimeError("Experiment run is already completed")
    if run.current_sol >= run.observation_window:
        run.status = "completed"
        raise RuntimeError("Experiment observation window is complete")

    run.status = "running"
    previous_history_len = len(run.world.get("history", []))
    tick(run.world, run.agents)
    observation = capture_observation(run.run_id, run.experiment_id, run.world, run.agents)
    run.observations.append(observation)

    history = run.world.get("history", [])
    if history:
        latest = copy.deepcopy(history[-1])
        # The simulation keeps only the latest 100 history records, so collect events here.
        if len(history) != previous_history_len or not run.events or run.events[-1].get("day") != latest.get("day"):
            run.events.append(latest)

    if run.current_sol >= run.observation_window:
        run.status = "completed"
    return observation


def run_experiment(
    experiment: dict[str, Any] | None = None,
    *,
    root: Path = ROOT,
) -> ExperimentRun:
    run = create_run(experiment, root=root)
    while run.status != "completed":
        step_run(run)
    return run
