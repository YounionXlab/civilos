from __future__ import annotations

from typing import Any


def evidence_can_support_promotion(item: dict[str, Any]) -> bool:
    """Only reviewed/verified external evidence is eligible for promotion review.

    Eligibility does not itself promote any insight; promotion remains an explicit
    separate decision governed by promotion.py.
    """
    return item.get("verification_status") in {"reviewed", "verified"}


def evidence_links(item: dict[str, Any]) -> dict[str, list[str]]:
    return {
        "questions": list(item.get("linked_questions", [])),
        "experiments": list(item.get("linked_experiments", [])),
        "insights": list(item.get("linked_insights", [])),
    }
