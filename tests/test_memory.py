import json
from pathlib import Path

from packages.engine.simulation import tick

ROOT = Path(__file__).resolve().parents[1]


def test_meaningful_event_creates_structured_memory():
    world = json.loads((ROOT / "data" / "world.json").read_text(encoding="utf-8"))
    citizens = json.loads((ROOT / "data" / "agents.json").read_text(encoding="utf-8"))

    tick(world, citizens)

    memories = [memory for citizen in citizens for memory in citizen["memories"]]
    assert len(memories) == 1
    assert memories[0]["day"] == 2
    assert memories[0]["type"] == "civilization_event"
    assert "Botanists harvested food" in memories[0]["description"]
    assert "food +3" in memories[0]["impact"]


def test_unrelated_event_does_not_create_memory():
    world = json.loads((ROOT / "data" / "world.json").read_text(encoding="utf-8"))
    world["day"] = 3
    citizens = [
        citizen
        for citizen in json.loads(
            (ROOT / "data" / "agents.json").read_text(encoding="utf-8")
        )
        if citizen["profession"] == "Doctor"
    ]

    tick(world, citizens)

    assert all(not citizen["memories"] for citizen in citizens)
