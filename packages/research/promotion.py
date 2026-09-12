from __future__ import annotations

EVIDENCE_ORDER = {f"E{i}": i for i in range(6)}


class PromotionError(ValueError):
    pass


def validate_insight_promotion(insight: dict) -> None:
    status = insight.get("status")
    level = insight.get("evidence_level")
    if level is None:
        if status in {"supported", "validated"}:
            raise PromotionError(f"{status} insight requires an evidence_level")
        return
    if level not in EVIDENCE_ORDER:
        raise PromotionError(f"Unknown evidence level: {level}")

    rank = EVIDENCE_ORDER[level]
    replications = int(insight.get("replications", 0))
    external = insight.get("external_datasets", [])
    independent = bool(insight.get("independent_replication", False))

    if status == "provisional" and rank < 1:
        raise PromotionError("provisional insight requires E1 or higher")
    if status == "supported":
        if rank < 2:
            raise PromotionError("supported insight requires E2 or higher")
        if replications < 1:
            raise PromotionError("supported insight requires reproducibility/replication evidence")
    if status == "validated":
        if rank < 3:
            raise PromotionError("validated insight requires E3 or higher")
        if not external and not independent:
            raise PromotionError("validated insight requires external evidence or independent replication")
