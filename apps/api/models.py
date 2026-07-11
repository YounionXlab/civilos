from typing import Any

from pydantic import BaseModel, Field


class CitizenModel(BaseModel):
    id: str
    name: str
    profession: str
    goal: str
    mood: str
    energy: int = Field(ge=0, le=100)
    current_task: str
    last_log: str
    memories: list[dict[str, Any]] = Field(default_factory=list)


class CitizensData(BaseModel):
    count: int
    items: list[CitizenModel]


class ChronicleEvent(BaseModel):
    day: int
    title: str
    description: str
    impact: dict[str, float | int] = Field(default_factory=dict)


class HistoryData(BaseModel):
    count: int
    items: list[ChronicleEvent]


class WorldData(BaseModel):
    day: int = 0
    planet: str = ""
    city: str = ""
    population: int = 0
    energy: int | float = 0
    water: int | float = 0
    food: int | float = 0
    technology: int | float = 0
    cq: float = 0
    history: list[ChronicleEvent] = Field(default_factory=list)


class WorldResponse(BaseModel):
    status: str
    message: str
    data: WorldData


class CitizensResponse(BaseModel):
    status: str
    message: str
    data: CitizensData


class HistoryResponse(BaseModel):
    status: str
    message: str
    data: HistoryData


class TickData(BaseModel):
    day: int
    world: WorldData
    citizens: CitizensData


class TickResponse(BaseModel):
    status: str
    message: str
    data: TickData


class HealthData(BaseModel):
    name: str
    version: str


class HealthResponse(BaseModel):
    status: str
    message: str
    data: HealthData
