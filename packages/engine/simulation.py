from typing import Any

from .events import chronicle_event
from .migrations import migrate_citizens
from .storage import Storage


def clamp(value: float, minimum: float = 0, maximum: float = 100) -> float:
    return max(minimum, min(maximum, value))


def agent_contribution(agent: dict[str, Any]) -> dict[str, float]:
    profession = agent.get("profession", agent.get("role", "")).lower()
    if "fusion" in profession:
        return {"energy": 3, "technology": 1}
    if "botanist" in profession:
        return {"food": 3, "water": -1}
    return {"cq": 0.01}


def update_agent(agent: dict[str, Any], world: dict[str, Any], index: int) -> None:
    day = int(world["day"])
    profession = agent["profession"].lower()
    tasks = (
        ["Calibrate fusion controls", "Review reactor telemetry", "Inspect power conduits"]
        if "fusion" in profession
        else ["Monitor greenhouse crops", "Test nutrient balance", "Prepare the next harvest"]
    )
    agent["current_task"] = tasks[(day + index) % len(tasks)]
    agent["energy"] = int(clamp(agent["energy"] - 6 + (day + index) % 4, 0, 100))
    if agent["energy"] >= 65:
        agent["mood"] = "focused"
    elif agent["energy"] >= 40:
        agent["mood"] = "steady"
    else:
        agent["mood"] = "tired"
    agent["last_log"] = (
        f"Day {day}: {agent['current_task']}. Energy is {agent['energy']} and mood is {agent['mood']}."
    )


def apply_impact(world: dict[str, Any], impact: dict[str, float]) -> None:
    for key, value in impact.items():
        world[key] = round(world.get(key, 0) + value, 2)


def tick(world: dict[str, Any], agents: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    agents = agents or []
    world["day"] = world.get("day", 0) + 1
    world["energy"] = world.get("energy", 0) - 4
    world["water"] = world.get("water", 0) - 2
    world["food"] = world.get("food", 0) - 3

    for agent in agents:
        for key, value in agent_contribution(agent).items():
            world[key] = world.get(key, 0) + value

    event = chronicle_event(world, agents)
    apply_impact(world, event["impact"])

    scarcity_count = sum(1 for key in ("energy", "water", "food") if world.get(key, 0) < 35)
    world["cq"] = round(clamp(world.get("cq", 0.4) + 0.01 - scarcity_count * 0.03, 0, 1), 2)
    for key in ("technology", "energy", "water", "food"):
        world[key] = clamp(world.get(key, 0), 0, 100)

    if scarcity_count >= 2:
        world["population"] = max(0, world.get("population", 0) - 1)
    elif world["food"] > 80 and world["water"] > 70 and world["cq"] > 0.55:
        world["population"] = world.get("population", 0) + 1

    for index, agent in enumerate(agents):
        update_agent(agent, world, index)

    world.setdefault("history", []).append(event)
    world["history"] = world["history"][-100:]
    return world


def advance_one_day() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    with Storage.transaction() as state:
        world = state["world"]
        agents = migrate_citizens(state["agents"])
        updated_world = tick(world, agents)
        state["world"] = updated_world
        state["agents"] = agents
        return updated_world, agents
