from fastapi import APIRouter

from apps.api.models import WorldResponse
from packages.engine.storage import Storage

router = APIRouter()


@router.get("/world", response_model=WorldResponse)
def get_world():
    return {
        "status": "ok",
        "message": "World state loaded.",
        "data": Storage.load_world(),
    }
