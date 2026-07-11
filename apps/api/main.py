from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from apps.api.routes.agents import router as agents_router
from apps.api.routes.history import router as history_router
from apps.api.routes.tick import router as tick_router
from apps.api.routes.world import router as world_router
from apps.api.models import HealthResponse
from packages.engine.storage import StorageError

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


@app.exception_handler(StorageError)
def storage_error_handler(_: Request, exc: StorageError):
    return JSONResponse(
        status_code=500,
        content={"error": "storage_error", "message": str(exc)},
    )


@app.get("/", response_model=HealthResponse)
def health_check():
    return {
        "status": "ok",
        "message": "CivilOS API is online.",
        "data": {"name": "CivilOS API", "version": "0.2.0"},
    }
