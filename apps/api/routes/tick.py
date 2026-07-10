from fastapi import APIRouter

from apps.api.models import TickResponse
from packages.engine.simulation import advance_one_day as run_simulation_tick

router = APIRouter()


@router.post("/tick", response_model=TickResponse)
def advance_one_day():
    updated, agents = run_simulation_tick()
    return {
        "status": "ok",
        "message": "Civilization advanced by one day.",
        "data": {
            "day": updated["day"],
            "world": updated,
            "agents": {"count": len(agents), "items": agents},
        },
    }
