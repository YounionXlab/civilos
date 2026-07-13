from copy import deepcopy
from typing import Any

from .citizens import Citizen


def migrate_citizen(source: dict[str, Any]) -> dict[str, Any]:
    citizen = deepcopy(source)
    citizen["profession"] = citizen.get("profession", citizen.pop("role", "Citizen"))
    legacy_goals = citizen.pop("goals", [])
    citizen["goal"] = citizen.get(
        "goal", legacy_goals[0] if legacy_goals else "Support the colony"
    )
    legacy_energy = citizen.pop("needs", {}).get("energy", 0.7) * 100
    citizen["energy"] = int(citizen.get("energy", legacy_energy))
    citizen.setdefault("mood", "steady")
    citizen.setdefault("current_task", "Review colony systems")
    citizen.setdefault("last_log", "Ready for the next simulation day.")
    citizen.setdefault("aliases", [])
    citizen.setdefault("age", 30)
    citizen.setdefault("gender", "unspecified")
    citizen.setdefault("birth_sol", 0)
    citizen.setdefault("skills", [])
    citizen.setdefault("traits", [])
    citizen.setdefault("personality", "adaptable")
    citizen.setdefault("health", 90)
    citizen.setdefault("memories", [])
    citizen.setdefault("relationships", {})
    return Citizen.from_dict(citizen).to_dict()


def migrate_citizens(citizens: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [migrate_citizen(citizen) for citizen in citizens]
