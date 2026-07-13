from typing import Any

from .citizens import Citizen, Memory
from .professions import ProfessionAction


def record_meaningful_memory(
    citizens: list[Citizen],
    actions: list[ProfessionAction],
    event: dict[str, Any],
) -> Citizen | None:
    impacted_resources = set(event.get("event_impact", {}))
    candidates = [
        (citizen, action)
        for citizen, action in zip(citizens, actions)
        if impacted_resources.intersection(action.resource_impact)
    ]
    if not candidates:
        return None

    citizen, action = candidates[(int(event["day"]) - 1) % len(candidates)]
    impact = ", ".join(
        f"{resource} {value:+g}" for resource, value in event["event_impact"].items()
    )
    citizen.memories.append(
        Memory(
            day=int(event["day"]),
            type="civilization_event",
            description=f"{action.task}. {event['title']}",
            impact=impact,
        )
    )
    citizen.memories = citizen.memories[-20:]
    return citizen
