from __future__ import annotations

import pytest

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
