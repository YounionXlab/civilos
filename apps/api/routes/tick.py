from fastapi import APIRouter

from packages.engine.simulation import tick
from packages.engine.storage import Storage

router = APIRouter()


@router.post("/tick")
def advance_one_day():
    world = Storage.load_world()
    agents = Storage.load_agents()
    updated = tick(world, agents)
    Storage.save_world(updated)
    Storage.save_agents(agents)
    return {
        "message": "Civilization advanced by one day.",
        "day": updated["day"],
        "world": updated,
        "agents": {"count": len(agents), "items": agents},
    }
