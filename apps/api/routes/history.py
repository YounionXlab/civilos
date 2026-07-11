from fastapi import APIRouter, Query

from apps.api.models import HistoryResponse
from packages.engine.storage import Storage

router = APIRouter()


@router.get("/history", response_model=HistoryResponse)
def get_history(limit: int = Query(default=30, ge=1, le=100)):
    world = Storage.load_world()
    history = world.get("history", [])
    return {
        "status": "ok",
        "message": "Civilization chronicle loaded.",
        "data": {"items": list(reversed(history[-limit:])), "count": len(history)},
    }
