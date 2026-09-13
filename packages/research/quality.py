from __future__ import annotations

from typing import Mapping

EQS_DIMENSIONS = (
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
)


def calculate_eqs(dimensions: Mapping[str, int]) -> int:
    missing = [key for key in EQS_DIMENSIONS if key not in dimensions]
    extra = sorted(set(dimensions) - set(EQS_DIMENSIONS))
    if missing:
        raise ValueError(f"Missing EQS dimensions: {', '.join(missing)}")
    if extra:
        raise ValueError(f"Unknown EQS dimensions: {', '.join(extra)}")
    values = []
    for key in EQS_DIMENSIONS:
        value = dimensions[key]
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 10:
            raise ValueError(f"EQS dimension {key} must be an integer from 0 to 10")
        values.append(value)
    return sum(values)


def validate_eqs(score: int | None, dimensions: Mapping[str, int] | None) -> None:
    if score is None and dimensions is None:
        return
    if score is None or dimensions is None:
        raise ValueError("quality_score and quality_dimensions must be provided together")
    calculated = calculate_eqs(dimensions)
    if score != calculated:
        raise ValueError(f"quality_score {score} does not equal EQS dimension sum {calculated}")
