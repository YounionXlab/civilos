from fastapi import APIRouter

from packages.engine.storage import Storage

router = APIRouter()


@router.get("/agents")
def get_agents():
    agents = Storage.load_agents()
    return {"count": len(agents), "items": agents}
