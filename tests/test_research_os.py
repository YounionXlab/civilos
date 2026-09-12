from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

from packages.research.promotion import PromotionError, validate_insight_promotion
from packages.research.quality import calculate_eqs, validate_eqs


def test_eqs_is_sum_of_ten_dimensions():
    dimensions = {
        "question_clarity": 8,
        "falsifiability": 7,
        "control_quality": 8,
        "variable_isolation": 7,
        "sample_size_repetitions": 5,
        "measurement_validity": 6,
        "statistical_rigor": 5,
        "reproducibility": 10,
        "robustness_sensitivity": 7,
        "external_validity": 2,
    }
    assert calculate_eqs(dimensions) == 65
    validate_eqs(65, dimensions)


def test_eqs_rejects_inconsistent_total():
    dimensions = {key: 5 for key in (
        "question_clarity",
        "falsifiability",
        "control_quality",
        "variable_isolation",
        "sample_size_repetitions",
        "measurement_validity",
        "statistical_rigor",
        "reproducibility",
        "robustness_sensitivity",
        "external_validity",
    )}
    with pytest.raises(ValueError, match="does not equal"):
        validate_eqs(60, dimensions)


def test_supported_insight_requires_e2_and_replication():
    with pytest.raises(PromotionError):
        validate_insight_promotion({"status": "supported", "evidence_level": "E1", "replications": 2})
    with pytest.raises(PromotionError):
        validate_insight_promotion({"status": "supported", "evidence_level": "E2", "replications": 0})
    validate_insight_promotion({"status": "supported", "evidence_level": "E2", "replications": 1})


def test_validated_insight_requires_external_or_independent_evidence():
    with pytest.raises(PromotionError):
        validate_insight_promotion({
            "status": "validated",
            "evidence_level": "E3",
            "replications": 2,
            "external_datasets": [],
            "independent_replication": False,
        })
    validate_insight_promotion({
        "status": "validated",
        "evidence_level": "E3",
        "replications": 2,
        "external_datasets": ["dataset-doi:example"],
        "independent_replication": False,
    })


def _load_json(path: str):
    with (ROOT / path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_canonical_question_registry_has_63_unique_ids():
    registry = _load_json("research/canonical_question_refs.json")
    ids = [item["id"] for item in registry["questions"]]
    assert len(ids) == 63
    assert len(set(ids)) == 63


def test_legacy_question_migration_is_complete():
    legacy = _load_json("research/questions.json")["questions"]
    migration = _load_json("research/question_id_migration_v2.json")["mappings"]
    assert len(migration) == len(legacy) == 30
    assert {item["legacy_id"] for item in migration} == {
        f"LEGACY-Q-{index:03d}" for index in range(1, 31)
    }


def test_ares_alpha_uses_canonical_mars_question():
    assert _load_json("experiments/exp-001-ares-alpha.json")["questions"] == ["Q-036"]
    assert _load_json("research/preregistrations/pre-exp-civ-001-001.json")[
        "research_question_ids"
    ] == ["Q-036"]
    assert _load_json("research/packages/pkg-civ-001.json")["question_ids"] == ["Q-036"]
    assert _load_json("research/evidence_items/evi-civ-001.json")["linked_questions"] == ["Q-036"]
    assert _load_json("insights/ins-001-ares-alpha-baseline.json")["source_questions"] == ["Q-036"]
