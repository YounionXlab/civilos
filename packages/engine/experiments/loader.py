from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_EXPERIMENT = ROOT / "experiments" / "exp-001-ares-alpha.json"
SCHEMA_PATH = ROOT / "schemas" / "experiment.schema.json"


class ExperimentDefinitionError(ValueError):
    pass


def load_experiment(path: str | Path = DEFAULT_EXPERIMENT) -> dict[str, Any]:
    experiment_path = Path(path)
    if not experiment_path.is_absolute():
        experiment_path = ROOT / experiment_path
    with experiment_path.open("r", encoding="utf-8") as handle:
        experiment = json.load(handle)
    with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(experiment),
        key=lambda error: list(error.path),
    )
    if errors:
        details = "; ".join(
            f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ExperimentDefinitionError(details)
    return experiment
