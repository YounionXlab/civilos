from .events import event_for_world
from .storage import Storage


def load_world():
    return Storage.load_world()


def save_world(world):
    Storage.save_world(world)


def load_agents():
    return Storage.load_agents()


def save_agents(agents):
    Storage.save_agents(agents)


def advance_one_day():
    world = load_world()
    agents = load_agents()
    updated = tick(world, agents)
    save_world(updated)
    save_agents(agents)
    return updated, agents


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


def agent_contribution(agent):
    role = agent.get("role", "").lower()
    if "fusion" in role:
        return {"energy": 3, "technology": 1}
    if "botanist" in role:
        return {"food": 3, "water": -1}
    return {"cq": 0.01}


def update_agent(agent, world):
    needs = agent.setdefault("needs", {})
    resource_pressure = (
        world.get("energy", 0) + world.get("water", 0) + world.get("food", 0)
    ) / 300
    needs["energy"] = round(clamp(needs.get("energy", 0.6) - 0.04 + resource_pressure * 0.03, 0, 1), 2)
    needs["rest"] = round(clamp(needs.get("rest", 0.6) - 0.03, 0, 1), 2)
    needs["social"] = round(clamp(needs.get("social", 0.5) + world.get("cq", 0.4) * 0.02, 0, 1), 2)
    agent.setdefault("memories", []).append(
        {
            "day": world["day"],
            "summary": f"Worked through day {world['day']} in {world.get('city', 'the colony')}.",
        }
    )
    agent["memories"] = agent["memories"][-10:]
    return agent


def tick(world, agents=None):
    agents = agents or []
    previous = {
        "population": world.get("population", 0),
        "energy": world.get("energy", 0),
        "water": world.get("water", 0),
        "food": world.get("food", 0),
        "technology": world.get("technology", 0),
        "cq": world.get("cq", 0),
    }

    world["day"] = world.get("day", 0) + 1
    world["energy"] = world.get("energy", 0) - 4
    world["water"] = world.get("water", 0) - 2
    world["food"] = world.get("food", 0) - 3

    for agent in agents:
        for key, value in agent_contribution(agent).items():
            world[key] = world.get(key, 0) + value

    scarcity_count = sum(1 for key in ("energy", "water", "food") if world.get(key, 0) < 35)
    world["cq"] = round(clamp(world.get("cq", 0.4) + 0.01 - scarcity_count * 0.03, 0, 1), 2)
    world["technology"] = clamp(world.get("technology", 0), 0, 100)
    world["energy"] = clamp(world.get("energy", 0), 0, 100)
    world["water"] = clamp(world.get("water", 0), 0, 100)
    world["food"] = clamp(world.get("food", 0), 0, 100)

    if scarcity_count >= 2:
        world["population"] = max(0, world.get("population", 0) - 1)
    elif world["food"] > 80 and world["water"] > 70 and world["cq"] > 0.55:
        world["population"] = world.get("population", 0) + 1

    for agent in agents:
        update_agent(agent, world)

    deltas = {
        key: round(world.get(key, 0) - previous[key], 2)
        for key in previous
        if world.get(key, 0) != previous[key]
    }
    world.setdefault("history", []).append(
        {
            "day": world["day"],
            "title": event_for_world(world),
            "deltas": deltas,
            "population": world.get("population", 0),
            "cq": world.get("cq", 0),
        }
    )
    world["history"] = world["history"][-100:]
    return world


if __name__ == "__main__":
    w = load_world()
    a = load_agents()
    save_world(tick(w, a))
    save_agents(a)
    print(f"Day {w['day']} complete")
