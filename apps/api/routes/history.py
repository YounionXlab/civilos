from fastapi import APIRouter, Query

from packages.engine.storage import Storage

router = APIRouter()


@router.get("/history")
def get_history(limit: int = Query(default=30, ge=1, le=100)):
    world = Storage.load_world()
    history = world.get("history", [])
    return {"items": history[-limit:], "count": len(history)}
