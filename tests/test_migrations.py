import json
from pathlib import Path

from packages.engine.migrations import migrate_citizen


def test_legacy_citizen_migration_is_separate_and_complete():
    legacy = {
        "id": "lin_yuan",
        "name": "Lin Yuan",
        "role": "Fusion Engineer",
        "goals": ["Upgrade reactor"],
        "needs": {"energy": 0.8},
    }
    citizen = migrate_citizen(legacy)
    assert citizen["profession"] == "Fusion Engineer"
    assert citizen["goal"] == "Upgrade reactor"
    assert citizen["energy"] == 80
    assert citizen["current_task"]
    assert "role" not in citizen
    assert legacy["role"] == "Fusion Engineer"


def test_seed_contains_twenty_complete_citizens():
    data_path = Path(__file__).resolve().parents[1] / "data" / "agents.json"
    citizens = json.loads(data_path.read_text(encoding="utf-8"))
    required = {
        "id",
        "name",
        "profession",
        "goal",
        "mood",
        "energy",
        "current_task",
        "health",
        "memories",
        "relationships",
    }
    assert len(citizens) == 20
    assert all(required <= citizen.keys() for citizen in citizens)
