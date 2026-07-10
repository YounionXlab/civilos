import random

EVENTS = [
    "Fusion reactor maintenance completed.",
    "Greenhouse harvest increased.",
    "Dust storm approaching.",
    "Water recycling efficiency improved.",
    "Citizen submitted a proposal.",
    "Research project started.",
]


def random_event() -> str:
    return random.choice(EVENTS)


def event_for_world(world: dict) -> str:
    if world.get("energy", 0) < 25:
        return "Energy reserves are critically low."
    if world.get("water", 0) < 25:
        return "Water rationing protocols activated."
    if world.get("food", 0) < 25:
        return "Greenhouse output is below survival targets."
    if world.get("cq", 0) >= 0.7:
        return "Civic coordination is improving daily operations."
    return random_event()
