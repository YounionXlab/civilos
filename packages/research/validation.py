from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


class ResearchDataError(ValueError):
    pass


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _validate(instance: Any, schema_path: Path, label: str) -> None:
    schema = _load_json(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        details = "; ".join(
            f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}" for error in errors
        )
        raise ResearchDataError(f"{label} failed schema validation: {details}")


def _ensure_unique(values: list[str], label: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        raise ResearchDataError(f"Duplicate {label}: {', '.join(duplicates)}")


def validate_research_data(root: Path = ROOT) -> None:
    questions_doc = _load_json(root / "research" / "questions.json")
    mappings_doc = _load_json(root / "research" / "mappings.json")

    questions = questions_doc.get("questions", [])
    question_ids = [item["id"] for item in questions]
    _ensure_unique(question_ids, "question IDs")

    question_schema = root / "schemas" / "question.schema.json"
    for item in questions:
        _validate(item, question_schema, f"question {item.get('id', '<unknown>')}")

    experiment_registry = mappings_doc.get("experiments", {})
    experiment_ids = list(experiment_registry)
    _ensure_unique(experiment_ids, "experiment IDs")

    mapping_question_ids = [item["question_id"] for item in mappings_doc.get("mappings", [])]
    _ensure_unique(mapping_question_ids, "mapping question IDs")

    question_id_set = set(question_ids)
    experiment_id_set = set(experiment_ids)

    for mapping in mappings_doc.get("mappings", []):
        question_id = mapping["question_id"]
        if question_id not in question_id_set:
            raise ResearchDataError(f"Unknown question reference: {question_id}")
        for experiment_id in mapping.get("experiments", []):
            if experiment_id not in experiment_id_set:
                raise ResearchDataError(f"Unknown experiment reference: {experiment_id}")

    for item in questions:
        for experiment_id in item.get("active_experiments", []):
            if experiment_id not in experiment_id_set:
                raise ResearchDataError(
                    f"Question {item['id']} references unknown experiment {experiment_id}"
                )

    experiment_schema = root / "schemas" / "experiment.schema.json"
    experiment_files = sorted((root / "experiments").glob("*.json"))
    canonical_definitions: dict[str, dict[str, Any]] = {}
    aliases: dict[str, str] = {}

    for path in experiment_files:
        experiment = _load_json(path)
        _validate(experiment, experiment_schema, f"experiment {path.name}")
        experiment_id = experiment["id"]
        if experiment_id in canonical_definitions:
            raise ResearchDataError(f"Duplicate canonical experiment definition: {experiment_id}")
        canonical_definitions[experiment_id] = experiment
        for alias in experiment.get("legacy_aliases", []):
            if alias in aliases:
                raise ResearchDataError(f"Duplicate experiment alias: {alias}")
            aliases[alias] = experiment_id

    for experiment_id, registration in experiment_registry.items():
        if registration.get("status") == "active" and experiment_id not in canonical_definitions:
            raise ResearchDataError(
                f"Active experiment {experiment_id} has no canonical definition"
            )

    if aliases.get("EXP-001") not in (None, "EXP-CIV-001"):
        raise ResearchDataError("EXP-001 must only alias EXP-CIV-001")

    insight_schema = root / "schemas" / "insight.schema.json"
    insights_dir = root / "insights"
    if insights_dir.exists():
        for path in sorted(insights_dir.glob("*.json")):
            _validate(_load_json(path), insight_schema, f"insight {path.name}")


if __name__ == "__main__":
    validate_research_data()
    print("Research data validation passed.")
