from fastapi import APIRouter

from packages.engine.storage import Storage

router = APIRouter()


@router.get("/history")
def get_history(limit: int = 30):
    world = Storage.load("world", default={})
    history = world.get("history", [])
    return {"items": history[-limit:], "count": len(history)}
