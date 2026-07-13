import hashlib
from typing import Any

from .citizens import Citizen
from .events import chronicle_event
from .migrations import migrate_citizens
from .memory import record_meaningful_memory
from .professions import ProfessionAction, behavior_for
from .storage import Storage

TRACKED_METRICS = ("population", "energy", "water", "food", "technology", "cq")


def clamp(value: float, minimum: float = 0, maximum: float = 100) -> float:
    return max(minimum, min(maximum, value))


def snapshot(world: dict[str, Any]) -> dict[str, float | int]:
    return {key: world.get(key, 0) for key in TRACKED_METRICS}


def apply_delta(world: dict[str, Any], delta: dict[str, float]) -> None:
    for key, value in delta.items():
        world[key] = round(world.get(key, 0) + value, 2)


def actions_for(citizens: list[Citizen], day: int) -> list[ProfessionAction]:
    return [
        behavior_for(citizen.profession).action_for(day, index)
        for index, citizen in enumerate(citizens)
    ]


def production_for(actions: list[ProfessionAction]) -> dict[str, float]:
    production: dict[str, float] = {}
    for action in actions:
        for key, value in action.resource_impact.items():
            production[key] = production.get(key, 0) + value
    return production


def update_citizen(
    citizen: Citizen, action: ProfessionAction, world: dict[str, Any], index: int
) -> None:
    day = int(world["day"])
    citizen.current_task = action.task
    recovery = 4 if day % 7 == index % 7 else 0
    citizen.energy = int(
        clamp(citizen.energy - 2 + (day + index) % 4 + recovery, 0, 100)
    )
    citizen.health = int(clamp(citizen.health + action.health_delta, 0, 100))
    citizen.mood = "focused" if citizen.energy >= 65 else "steady" if citizen.energy >= 40 else "tired"


def deterministic_roll(world: dict[str, Any]) -> float:
    seed = world.get("seed", "ARES-ALPHA-001")
    value = f"{seed}:{world['day']}:{world['population']}".encode()
    return int(hashlib.sha256(value).hexdigest()[:8], 16) / 0xFFFFFFFF


def update_population(world: dict[str, Any]) -> dict[str, Any]:
    day = int(world["day"])
    roll = deterministic_roll(world)
    cooldown_until = int(world.get("population_cooldown_until", 0))
    if day < cooldown_until:
        return {"delta": 0, "reason": f"Population cooldown active until day {cooldown_until}.", "roll": roll}

    healthy = min(world[resource] for resource in ("energy", "water", "food")) >= 70 and world["cq"] >= 0.5
    critical = sum(world[resource] < 20 for resource in ("energy", "water", "food")) >= 2
    if healthy and roll < 0.002:
        world["population"] += 1
        world["population_cooldown_until"] = day + 90
        return {"delta": 1, "reason": "High reserves and civic coordination supported a birth.", "roll": roll}
    if critical and roll < 0.02:
        world["population"] = max(0, world["population"] - 1)
        world["population_cooldown_until"] = day + 30
        return {"delta": -1, "reason": "Sustained critical shortages caused a population loss.", "roll": roll}
    return {"delta": 0, "reason": "No demographic threshold produced a change.", "roll": roll}


def tick(world: dict[str, Any], agents: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    source_agents = agents
    citizens = [Citizen.from_dict(record) for record in (agents or [])]
    before = snapshot(world)
    world["day"] = world.get("day", 0) + 1

    population = world.get("population", len(agents))
    daily_delta = {
        "energy": -0.30 * population,
        "water": -0.25 * population,
        "food": -0.24 * population,
    }
    actions = actions_for(citizens, int(world["day"]))
    for key, value in production_for(actions).items():
        daily_delta[key] = daily_delta.get(key, 0) + value
    apply_delta(world, daily_delta)

    citizen_records = [citizen.to_dict() for citizen in citizens]
    event = chronicle_event(world, citizen_records)
    event["day"] = world["day"]
    apply_delta(world, event["event_impact"])
    scarcity_count = sum(world[key] < 35 for key in ("energy", "water", "food"))
    world["cq"] = round(clamp(world.get("cq", 0.4) - scarcity_count * 0.01, 0, 1), 2)
    for key in ("technology", "energy", "water", "food"):
        world[key] = round(clamp(world.get(key, 0), 0, 100), 2)

    population_change = update_population(world)
    for index, (citizen, action) in enumerate(zip(citizens, actions)):
        update_citizen(citizen, action, world, index)
    record_meaningful_memory(citizens, actions, event)

    after = snapshot(world)
    total_daily_delta = {
        key: round(after[key] - before[key], 2)
        for key in TRACKED_METRICS
        if after[key] != before[key]
    }
    world.setdefault("history", []).append(
        {
            "day": world["day"],
            "title": event["title"],
            "description": event["description"],
            "before": before,
            "after": after,
            "event_impact": event["event_impact"],
            "daily_delta": total_daily_delta,
            "population_change": population_change,
            "participant_professions": event.get("participant_professions", []),
            "participant_citizen_ids": event.get("participant_citizen_ids", []),
        }
    )
    world["history"] = world["history"][-100:]
    if source_agents is not None:
        source_agents[:] = [citizen.to_dict() for citizen in citizens]
    return world


def advance_one_day() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    with Storage.transaction() as state:
        world = state["world"]
        agents = migrate_citizens(state["agents"])
        updated_world = tick(world, agents)
        state["world"] = updated_world
        state["agents"] = agents
        return updated_world, agents
