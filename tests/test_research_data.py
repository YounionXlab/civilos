import json
import shutil
from pathlib import Path

import pytest

from packages.research.validation import ResearchDataError, validate_research_data

ROOT = Path(__file__).resolve().parents[1]


def _copy_research_fixture(tmp_path: Path) -> Path:
    for name in ("research", "schemas", "experiments"):
        shutil.copytree(ROOT / name, tmp_path / name)
    return tmp_path


def test_canonical_research_data_validates():
    validate_research_data(ROOT)


def test_duplicate_question_id_fails(tmp_path: Path):
    root = _copy_research_fixture(tmp_path)
    path = root / "research" / "questions.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["questions"].append(dict(document["questions"][0]))
    path.write_text(json.dumps(document, indent=2), encoding="utf-8")

    with pytest.raises(ResearchDataError, match="Duplicate question IDs"):
        validate_research_data(root)


def test_dangling_experiment_reference_fails(tmp_path: Path):
    root = _copy_research_fixture(tmp_path)
    path = root / "research" / "mappings.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["mappings"][0]["experiments"].append("EXP-CIV-999")
    path.write_text(json.dumps(document, indent=2), encoding="utf-8")

    with pytest.raises(ResearchDataError, match="Unknown experiment reference"):
        validate_research_data(root)


def test_malformed_experiment_fails(tmp_path: Path):
    root = _copy_research_fixture(tmp_path)
    path = root / "experiments" / "exp-001-ares-alpha.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document.pop("hypothesis")
    path.write_text(json.dumps(document, indent=2), encoding="utf-8")

    with pytest.raises(ResearchDataError, match="failed schema validation"):
        validate_research_data(root)


def test_legacy_ares_alias_points_to_canonical_id():
    document = json.loads(
        (ROOT / "experiments" / "exp-001-ares-alpha.json").read_text(encoding="utf-8")
    )
    assert document["id"] == "EXP-CIV-001"
    assert "EXP-001" in document["legacy_aliases"]
