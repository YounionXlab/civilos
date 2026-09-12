from __future__ import annotations

from pathlib import Path
from typing import Any


def package_paths_exist(package: dict[str, Any], root: Path) -> list[str]:
    """Return package-relative paths that do not exist in the repository."""
    missing: list[str] = []
    for field in ("result_paths", "report_paths"):
        for raw in package.get(field, []):
            path = root / raw
            if not path.exists():
                missing.append(raw)
    return sorted(set(missing))


def package_summary(package: dict[str, Any]) -> dict[str, Any]:
    """Return a stable, publication-oriented summary of a research package."""
    return {
        "package_id": package["package_id"],
        "title": package["title"],
        "questions": list(package.get("question_ids", [])),
        "experiments": list(package.get("experiment_ids", [])),
        "insights": list(package.get("insight_ids", [])),
        "external_evidence_items": list(package.get("evidence_item_ids", [])),
        "evidence_level": package["evidence_level"],
        "experiment_quality_score": package.get("experiment_quality_score"),
        "reproducibility_status": package["reproducibility_status"],
        "publication_status": package["publication_status"],
    }
