from fastapi import APIRouter

from apps.api.models import CitizensResponse
from packages.engine.storage import Storage

router = APIRouter()


@router.get("/agents", response_model=CitizensResponse)
def get_agents():
    agents = Storage.load_agents()
    return {
        "status": "ok",
        "message": "Citizens loaded.",
        "data": {"count": len(agents), "items": agents},
    }
