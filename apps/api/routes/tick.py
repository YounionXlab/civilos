from fastapi import APIRouter

from packages.engine.simulation import load_agents, load_world, save_agents, save_world, tick

router = APIRouter()


@router.post("/tick")
def advance_one_day():
    world = load_world()
    agents = load_agents()
    updated = tick(world, agents)
    save_world(updated)
    save_agents(agents)
    return {
        "message": "Civilization advanced by one day.",
        "day": updated["day"],
        "world": updated,
        "agents": {"count": len(agents), "items": agents},
    }
