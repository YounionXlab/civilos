from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .promotion import PromotionError, validate_insight_promotion
from .quality import validate_eqs

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
    question_id_set = set(question_ids)
    experiment_id_set = set(experiment_ids)

    mapping_question_ids = [item["question_id"] for item in mappings_doc.get("mappings", [])]
    _ensure_unique(mapping_question_ids, "mapping question IDs")
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
    canonical_definitions: dict[str, dict[str, Any]] = {}
    aliases: dict[str, str] = {}
    for path in sorted((root / "experiments").glob("*.json")):
        experiment = _load_json(path)
        _validate(experiment, experiment_schema, f"experiment {path.name}")
        experiment_id = experiment["id"]
        if experiment_id in canonical_definitions:
            raise ResearchDataError(f"Duplicate canonical experiment definition: {experiment_id}")
        canonical_definitions[experiment_id] = experiment
        try:
            validate_eqs(experiment.get("quality_score"), experiment.get("quality_dimensions"))
        except ValueError as exc:
            raise ResearchDataError(f"experiment {path.name} has invalid EQS: {exc}") from exc
        for alias in experiment.get("legacy_aliases", []):
            if alias in aliases:
                raise ResearchDataError(f"Duplicate experiment alias: {alias}")
            aliases[alias] = experiment_id

    for experiment_id, registration in experiment_registry.items():
        if registration.get("status") == "active" and experiment_id not in canonical_definitions:
            raise ResearchDataError(f"Active experiment {experiment_id} has no canonical definition")
    if aliases.get("EXP-001") not in (None, "EXP-CIV-001"):
        raise ResearchDataError("EXP-001 must only alias EXP-CIV-001")

    evidence_source_path = root / "research" / "evidence_sources.json"
    if evidence_source_path.exists():
        evidence_doc = _load_json(evidence_source_path)
        source_schema = root / "schemas" / "evidence_source.schema.json"
        sources = evidence_doc.get("sources", [])
        source_ids = [item["id"] for item in sources]
        _ensure_unique(source_ids, "evidence source IDs")
        for item in sources:
            _validate(item, source_schema, f"evidence source {item.get('id', '<unknown>')}")

    evidence_ids: set[str] = set()
    evidence_dir = root / "research" / "evidence"
    evidence_schema = root / "schemas" / "evidence_reference.schema.json"
    if evidence_dir.exists():
        for path in sorted(evidence_dir.glob("*.json")):
            item = _load_json(path)
            _validate(item, evidence_schema, f"evidence reference {path.name}")
            evidence_id = item["id"]
            if evidence_id in evidence_ids:
                raise ResearchDataError(f"Duplicate evidence reference ID: {evidence_id}")
            evidence_ids.add(evidence_id)
            for question_id in item.get("supports_questions", []):
                if question_id not in question_id_set:
                    raise ResearchDataError(f"Evidence {evidence_id} references unknown question {question_id}")
            for experiment_id in item.get("supports_experiments", []):
                if experiment_id not in experiment_id_set:
                    raise ResearchDataError(f"Evidence {evidence_id} references unknown experiment {experiment_id}")

    prereg_dir = root / "research" / "preregistrations"
    prereg_schema = root / "schemas" / "preregistration.schema.json"
    prereg_ids: list[str] = []
    if prereg_dir.exists():
        for path in sorted(prereg_dir.glob("*.json")):
            item = _load_json(path)
            _validate(item, prereg_schema, f"preregistration {path.name}")
            prereg_ids.append(item["id"])
            if item["experiment_id"] not in experiment_id_set:
                raise ResearchDataError(
                    f"Preregistration {item['id']} references unknown experiment {item['experiment_id']}"
                )
            for question_id in item["research_question_ids"]:
                if question_id not in question_id_set:
                    raise ResearchDataError(
                        f"Preregistration {item['id']} references unknown question {question_id}"
                    )
            for evidence_id in item.get("prior_evidence_ids", []):
                if evidence_id not in evidence_ids:
                    raise ResearchDataError(
                        f"Preregistration {item['id']} references unknown evidence {evidence_id}"
                    )
    _ensure_unique(prereg_ids, "preregistration IDs")

    insight_schema = root / "schemas" / "insight.schema.json"
    insights_dir = root / "insights"
    if insights_dir.exists():
        for path in sorted(insights_dir.glob("*.json")):
            insight = _load_json(path)
            _validate(insight, insight_schema, f"insight {path.name}")
            try:
                validate_insight_promotion(insight)
            except PromotionError as exc:
                raise ResearchDataError(f"insight {path.name} violates promotion rules: {exc}") from exc
            for evidence_id in insight.get("evidence_references", []):
                if evidence_id not in evidence_ids:
                    raise ResearchDataError(
                        f"Insight {insight['id']} references unknown evidence {evidence_id}"
                    )


if __name__ == "__main__":
    validate_research_data()
    print("Research data validation passed.")
