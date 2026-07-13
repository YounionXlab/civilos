import json
from copy import deepcopy
from pathlib import Path

from packages.engine.professions import GENERIC_BEHAVIOR, behavior_for
from packages.engine.simulation import TRACKED_METRICS, tick

ROOT = Path(__file__).resolve().parents[1]


def load_seed():
    world = json.loads((ROOT / "data" / "world.json").read_text(encoding="utf-8"))
    agents = json.loads((ROOT / "data" / "agents.json").read_text(encoding="utf-8"))
    return world, agents


def test_tick_creates_accurate_chronicle_and_updates_citizens():
    world, agents = load_seed()
    before = {key: world[key] for key in TRACKED_METRICS}

    updated_world = tick(world, agents)
    entry = updated_world["history"][-1]

    assert entry["before"] == before
    assert entry["after"] == {key: updated_world[key] for key in TRACKED_METRICS}
    assert entry["event_impact"] == {"food": 3}
    assert entry["daily_delta"] == {
        key: round(entry["after"][key] - entry["before"][key], 2)
        for key in TRACKED_METRICS
        if entry["after"][key] != entry["before"][key]
    }
    assert agents[0]["current_task"] != "Review daily priorities"


def test_tick_is_deterministic():
    world, agents = load_seed()
    first_world, first_agents = deepcopy(world), deepcopy(agents)
    second_world, second_agents = deepcopy(world), deepcopy(agents)
    assert tick(first_world, first_agents) == tick(second_world, second_agents)
    assert first_agents == second_agents


def test_profession_registry_has_generic_fallback():
    assert behavior_for("Unknown Profession") is GENERIC_BEHAVIOR


def test_professions_create_distinct_resource_impacts():
    fusion = behavior_for("Fusion Engineer").action_for(day=2, citizen_index=0)
    botanist = behavior_for("Botanist").action_for(day=2, citizen_index=0)
    doctor = behavior_for("Doctor").action_for(day=2, citizen_index=0)
    assert fusion.resource_impact["energy"] > 0
    assert botanist.resource_impact["food"] > 0
    assert doctor.health_delta > 0


def test_healthy_colony_remains_viable_for_one_thousand_ticks():
    world, agents = load_seed()
    minimum_resources = {"energy": 100.0, "water": 100.0, "food": 100.0}

    for _ in range(1000):
        tick(world, agents)
        for resource in minimum_resources:
            minimum_resources[resource] = min(minimum_resources[resource], world[resource])

    assert world["population"] > 0
    assert all(value >= 35 for value in minimum_resources.values())
    assert len(world["history"]) == 100
