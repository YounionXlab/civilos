from typing import Any


def chronicle_event(world: dict[str, Any], agents: list[dict[str, Any]]) -> dict[str, Any]:
    day = int(world["day"])
    event_index = day % 5
    if event_index == 0:
        return {
            "title": "Fusion reactor efficiency increased.",
            "description": "Engineering adjustments improved the colony's reactor output.",
            "event_impact": {"energy": 2, "technology": 1},
        }
    if event_index == 1:
        return {
            "title": "Water recycling cycle completed.",
            "description": "The recycling system recovered additional water for daily use.",
            "event_impact": {"water": 2},
        }
    if event_index == 2:
        return {
            "title": "Botanists harvested food.",
            "description": "The greenhouse team completed a productive harvest.",
            "event_impact": {"food": 3},
        }
    if event_index == 3 and agents:
        citizen = agents[(day - 1) % len(agents)]
        return {
            "title": f"Citizen {citizen['name']} proposed an operational upgrade.",
            "description": f"{citizen['name']} submitted a proposal related to {citizen['goal'].lower()}.",
            "event_impact": {"technology": 1, "cq": 0.01},
        }
    return {
        "title": "Dust storm reduced solar efficiency.",
        "description": "Airborne dust temporarily reduced auxiliary power generation.",
        "event_impact": {"energy": -2},
    }
