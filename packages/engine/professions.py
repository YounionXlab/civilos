from typing import Any

GENERIC_BEHAVIOR = {
    "production": {},
    "tasks": ["Inspect shared systems", "Support colony operations", "Review daily priorities"],
}

PROFESSION_BEHAVIORS: dict[str, dict[str, Any]] = {
    "fusion engineer": {
        "production": {"energy": 1.5, "technology": 0.05},
        "tasks": ["Calibrate fusion controls", "Review reactor telemetry", "Inspect power conduits"],
    },
    "botanist": {
        "production": {"food": 1.2},
        "tasks": ["Monitor greenhouse crops", "Test nutrient balance", "Prepare the next harvest"],
    },
    "water engineer": {
        "production": {"water": 1.25},
        "tasks": ["Inspect recycling filters", "Monitor reservoir quality", "Test purification output"],
    },
    "systems engineer": {
        "production": {"technology": 0.08},
        "tasks": ["Review habitat diagnostics", "Inspect life-support systems", "Review sensor alerts"],
    },
    "logistics coordinator": {
        "production": {"energy": 0.2, "water": 0.2, "food": 0.2},
        "tasks": ["Audit supply inventory", "Plan daily allocations", "Review delivery schedules"],
    },
    "medic": {
        "production": {},
        "tasks": ["Review health reports", "Check medical supplies", "Run wellness checks"],
    },
}


def behavior_for(profession: str) -> dict[str, Any]:
    return PROFESSION_BEHAVIORS.get(profession.lower(), GENERIC_BEHAVIOR)
