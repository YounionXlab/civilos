from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .package import package_paths_exist

ROOT = Path(__file__).resolve().parents[2]


class ResearchPackageError(ValueError):
    pass


def _load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _validate(instance: Any, schema_path: Path, label: str) -> None:
    validator = Draft202012Validator(_load(schema_path))
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        details = "; ".join(
            f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}" for error in errors
        )
        raise ResearchPackageError(f"{label} failed schema validation: {details}")


def _ids(root: Path, directory: str, key: str) -> set[str]:
    values: set[str] = set()
    path = root / directory
    if path.exists():
        for item_path in sorted(path.glob("*.json")):
            item = _load(item_path)
            value = item[key]
            if value in values:
                raise ResearchPackageError(f"Duplicate {key}: {value}")
            values.add(value)
    return values


def validate_research_packages(root: Path = ROOT) -> None:
    canonical_path = root / "research" / "canonical_question_refs.json"
    question_path = canonical_path if canonical_path.exists() else root / "research" / "questions.json"
    questions = _load(question_path).get("questions", [])
    question_ids = {item["id"] for item in questions}

    experiment_ids = set(_load(root / "research" / "mappings.json").get("experiments", {}))
    preregistration_ids = _ids(root, "research/preregistrations", "id")
    insight_ids = _ids(root, "insights", "id")

    evidence_ids: set[str] = set()
    evidence_dir = root / "research" / "evidence_items"
    evidence_schema = root / "schemas" / "evidence_item.schema.json"
    if evidence_dir.exists():
        for path in sorted(evidence_dir.glob("*.json")):
            item = _load(path)
            _validate(item, evidence_schema, f"evidence item {path.name}")
            evidence_id = item["evidence_id"]
            if evidence_id in evidence_ids:
                raise ResearchPackageError(f"Duplicate evidence item ID: {evidence_id}")
            evidence_ids.add(evidence_id)
            for question_id in item.get("linked_questions", []):
                if question_id not in question_ids:
                    raise ResearchPackageError(
                        f"Evidence item {evidence_id} references unknown question {question_id}"
                    )
            for experiment_id in item.get("linked_experiments", []):
                if experiment_id not in experiment_ids:
                    raise ResearchPackageError(
                        f"Evidence item {evidence_id} references unknown experiment {experiment_id}"
                    )
            for insight_id in item.get("linked_insights", []):
                if insight_id not in insight_ids:
                    raise ResearchPackageError(
                        f"Evidence item {evidence_id} references unknown insight {insight_id}"
                    )

    package_schema = root / "schemas" / "research_package.schema.json"
    package_dir = root / "research" / "packages"
    package_ids: set[str] = set()
    if package_dir.exists():
        for path in sorted(package_dir.glob("*.json")):
            package = _load(path)
            _validate(package, package_schema, f"research package {path.name}")
            package_id = package["package_id"]
            if package_id in package_ids:
                raise ResearchPackageError(f"Duplicate research package ID: {package_id}")
            package_ids.add(package_id)

            for question_id in package.get("question_ids", []):
                if question_id not in question_ids:
                    raise ResearchPackageError(
                        f"Package {package_id} references unknown question {question_id}"
                    )
            for prereg_id in package.get("preregistration_ids", []):
                if prereg_id not in preregistration_ids:
                    raise ResearchPackageError(
                        f"Package {package_id} references unknown preregistration {prereg_id}"
                    )
            for experiment_id in package.get("experiment_ids", []):
                if experiment_id not in experiment_ids:
                    raise ResearchPackageError(
                        f"Package {package_id} references unknown experiment {experiment_id}"
                    )
            for insight_id in package.get("insight_ids", []):
                if insight_id not in insight_ids:
                    raise ResearchPackageError(
                        f"Package {package_id} references unknown insight {insight_id}"
                    )
            for evidence_id in package.get("evidence_item_ids", []):
                if evidence_id not in evidence_ids:
                    raise ResearchPackageError(
                        f"Package {package_id} references unknown evidence item {evidence_id}"
                    )
            missing = package_paths_exist(package, root)
            if missing:
                raise ResearchPackageError(
                    f"Package {package_id} references missing paths: {', '.join(missing)}"
                )


if __name__ == "__main__":
    validate_research_packages()
    print("Research package validation passed.")
