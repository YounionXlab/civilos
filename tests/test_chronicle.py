from pathlib import Path

from packages.engine.chronicle import export_chronicle, generate_journal_entry


def test_generate_and_export_chronicle_drafts(tmp_path: Path):
    event = {
        "day": 12,
        "title": "First Reactor Breakthrough.",
        "description": "The colony reached a new milestone today.",
        "event_impact": {"energy": 3, "technology": 1},
        "daily_delta": {"energy": 3, "technology": 1},
    }
    citizens = [
        {
            "id": "lin_yuan",
            "name": "Lin Yuan",
            "profession": "Fusion Engineer",
            "current_task": "Complete a reactor optimization",
        }
    ]

    entry = generate_journal_entry(
        {"day": 12, "history": [event]}, citizens, event=event
    )
    paths = export_chronicle(entry, tmp_path)

    assert entry["sol"] == 12
    assert entry["citizens"] == ["Lin Yuan"]
    assert paths["markdown"] == tmp_path / "docs" / "chronicles" / "sol-0012.md"
    assert paths["social"] == tmp_path / "social" / "x" / "sol-0012.txt"
    assert paths["markdown"].exists()
    assert paths["social"].exists()
    assert "First Reactor Breakthrough" in paths["markdown"].read_text(encoding="utf-8")
    assert "Lin Yuan" in paths["social"].read_text(encoding="utf-8")


def test_simulation_does_not_depend_on_chronicle_exporter():
    simulation_source = (
        Path(__file__).resolve().parents[1] / "packages" / "engine" / "simulation.py"
    ).read_text(encoding="utf-8")
    assert "from .chronicle" not in simulation_source
    assert "engine.chronicle" not in simulation_source
