from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from packages.research.evidence import evidence_can_support_promotion
from packages.research.package_validation import ResearchPackageError, validate_research_packages

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_research_package_validates() -> None:
    validate_research_packages(ROOT)


def test_unreviewed_external_evidence_is_not_promotion_eligible() -> None:
    assert not evidence_can_support_promotion({"verification_status": "unreviewed"})
    assert evidence_can_support_promotion({"verification_status": "reviewed"})
    assert evidence_can_support_promotion({"verification_status": "verified"})


def test_dangling_result_path_fails(tmp_path: Path) -> None:
    # Minimal copy of the canonical package validation surface.
    for rel in [
        "research/questions.json",
        "research/mappings.json",
        "research/preregistrations/pre-exp-civ-001-001.json",
        "insights/ins-001-ares-alpha-baseline.json",
        "schemas/research_package.schema.json",
        "schemas/evidence_item.schema.json",
    ]:
        source = ROOT / rel
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    package = json.loads((ROOT / "research/packages/pkg-civ-001.json").read_text(encoding="utf-8"))
    package["result_paths"] = ["results/does-not-exist.json"]
    package_path = tmp_path / "research/packages/pkg-civ-001.json"
    package_path.parent.mkdir(parents=True, exist_ok=True)
    package_path.write_text(json.dumps(package), encoding="utf-8")

    with pytest.raises(ResearchPackageError, match="missing paths"):
        validate_research_packages(tmp_path)
