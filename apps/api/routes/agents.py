from fastapi import APIRouter

from fastapi.responses import JSONResponse

from apps.api.models import CitizenResponse, CitizensResponse, ErrorResponse
from packages.engine.citizens import Citizen
from packages.engine.storage import Storage

router = APIRouter()


@router.get("/agents", response_model=CitizensResponse)
def get_agents():
    agents = Storage.load_agents()
    items = []
    for record in agents:
        citizen = Citizen.from_dict(record)
        items.append(
            {
                "id": citizen.id,
                "name": citizen.name,
                "profession": citizen.profession,
                "mood": citizen.mood,
                "current_task": citizen.current_task,
                "latest_memory": (
                    citizen.latest_memory.__dict__ if citizen.latest_memory else None
                ),
            }
        )
    return {
        "status": "ok",
        "message": "Citizens loaded.",
        "data": {"count": len(items), "items": items},
    }


@router.get(
    "/agents/{citizen_id}",
    response_model=CitizenResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_agent(citizen_id: str):
    for record in Storage.load_agents():
        citizen = Citizen.from_dict(record)
        if citizen.id == citizen_id:
            data = citizen.to_dict()
            data["latest_memory"] = (
                citizen.latest_memory.__dict__ if citizen.latest_memory else None
            )
            return {
                "status": "ok",
                "message": "Citizen profile loaded.",
                "data": data,
            }
    return JSONResponse(
        status_code=404,
        content={"status": "error", "message": "Citizen not found.", "data": None},
    )
