from fastapi import APIRouter

from apps.api.models import AgentsResponse
from packages.engine.storage import Storage

router = APIRouter()


@router.get("/agents", response_model=AgentsResponse)
def get_agents():
    agents = Storage.load_agents()
    return {"count": len(agents), "items": agents}
