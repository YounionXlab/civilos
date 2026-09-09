from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import mean
from typing import Any


@dataclass(frozen=True)
class Observation:
    run_id: str
    experiment_id: str
    sol: int
    population: int
    energy: float
    water: float
    food: float
    technology: float
    cq: float
    citizen_health_mean: float
    citizen_energy_mean: float
    important_event_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def capture_observation(
    run_id: str,
    experiment_id: str,
    world: dict[str, Any],
    agents: list[dict[str, Any]],
) -> Observation:
    health_values = [float(agent.get("health", 0)) for agent in agents]
    energy_values = [float(agent.get("energy", 0)) for agent in agents]
    return Observation(
        run_id=run_id,
        experiment_id=experiment_id,
        sol=int(world.get("day", 0)),
        population=int(world.get("population", len(agents))),
        energy=float(world.get("energy", 0)),
        water=float(world.get("water", 0)),
        food=float(world.get("food", 0)),
        technology=float(world.get("technology", 0)),
        cq=float(world.get("cq", 0)),
        citizen_health_mean=round(mean(health_values), 2) if health_values else 0.0,
        citizen_energy_mean=round(mean(energy_values), 2) if energy_values else 0.0,
        important_event_count=1 if world.get("history") else 0,
    )
