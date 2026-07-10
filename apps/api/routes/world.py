from fastapi import APIRouter

from packages.engine.storage import Storage

router = APIRouter()


@router.get("/world")
def get_world():
    return Storage.load_world()
