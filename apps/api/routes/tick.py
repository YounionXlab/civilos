from fastapi import APIRouter

from packages.engine.simulation import load_world, save_world, tick

router = APIRouter()


@router.post("/tick")
def advance_one_day():
    world = load_world()
    updated = tick(world)
    save_world(updated)
    return {
        "message": "Civilization advanced by one day.",
        "day": updated["day"],
        "world": updated,
    }
