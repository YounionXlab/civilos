from copy import deepcopy

from packages.engine.simulation import tick


def test_tick_creates_chronicle_and_updates_citizens():
    world = {
        "day": 1,
        "population": 20,
        "energy": 82,
        "water": 77,
        "food": 91,
        "technology": 34,
        "cq": 0.42,
        "history": [],
    }
    agents = [
        {
            "id": "lin_yuan",
            "name": "Lin Yuan",
            "profession": "Fusion Engineer",
            "goal": "Upgrade Fusion Reactor",
            "mood": "focused",
            "energy": 80,
            "current_task": "Review reactor telemetry",
            "last_log": "Ready.",
        }
    ]

    updated_world = tick(deepcopy(world), agents)

    assert updated_world["day"] == 2
    assert updated_world["history"] == [
        {
            "day": 2,
            "title": "Botanists harvested food.",
            "description": "The greenhouse team completed a productive harvest.",
            "impact": {"food": 3},
        }
    ]
    assert agents[0]["energy"] != 80
    assert agents[0]["last_log"].startswith("Day 2:")


def test_tick_is_deterministic():
    world = {
        "day": 2,
        "population": 20,
        "energy": 80,
        "water": 75,
        "food": 90,
        "technology": 35,
        "cq": 0.43,
        "history": [],
    }
    agents = [
        {
            "id": "lin_yuan",
            "name": "Lin Yuan",
            "profession": "Fusion Engineer",
            "goal": "Upgrade Fusion Reactor",
            "energy": 75,
        }
    ]

    first = tick(deepcopy(world), deepcopy(agents))
    second = tick(deepcopy(world), deepcopy(agents))

    assert first == second
