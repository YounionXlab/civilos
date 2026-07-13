import json
from pathlib import Path

import pytest

from packages.engine.citizens import Citizen

ROOT = Path(__file__).resolve().parents[1]


def test_twenty_complete_unique_citizens_load():
    records = json.loads((ROOT / "data" / "agents.json").read_text(encoding="utf-8"))
    citizens = [Citizen.from_dict(record) for record in records]
    assert len(citizens) == 20
    assert len({citizen.id for citizen in citizens}) == 20
    assert len({citizen.name for citizen in citizens}) == 20
    assert {
        "Fusion Engineer",
        "Botanist",
        "Miner",
        "Doctor",
        "Researcher",
        "Technician",
        "Teacher",
        "Administrator",
    } <= {citizen.profession for citizen in citizens}


def test_citizen_model_validates_ranges():
    record = json.loads((ROOT / "data" / "agents.json").read_text(encoding="utf-8"))[0]
    record["health"] = 101
    with pytest.raises(ValueError, match="energy and health"):
        Citizen.from_dict(record)
