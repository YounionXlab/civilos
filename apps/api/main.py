from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.routes.agents import router as agents_router
from apps.api.routes.history import router as history_router
from apps.api.routes.tick import router as tick_router
from apps.api.routes.world import router as world_router

app = FastAPI(title="CivilOS API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(world_router)
app.include_router(agents_router)
app.include_router(history_router)
app.include_router(tick_router)


@app.get("/")
def health_check():
    return {"name": "CivilOS API", "version": "0.1.0", "status": "online"}
