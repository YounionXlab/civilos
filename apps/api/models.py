from typing import Any

from pydantic import BaseModel, Field


class MemoryModel(BaseModel):
    day: int
    type: str
    description: str
    impact: str


class RelationshipModel(BaseModel):
    type: str
    strength: float = Field(ge=0, le=1)


class CitizenSummary(BaseModel):
    id: str
    name: str
    profession: str
    mood: str
    current_task: str
    latest_memory: MemoryModel | None = None


class CitizenProfile(CitizenSummary):
    aliases: list[str]
    age: int = Field(ge=0)
    gender: str
    birth_sol: int = Field(ge=0)
    skills: list[str]
    traits: list[str]
    personality: str
    goal: str
    energy: int = Field(ge=0, le=100)
    health: int = Field(ge=0, le=100)
    memories: list[MemoryModel] = Field(default_factory=list)
    relationships: dict[str, RelationshipModel] = Field(default_factory=dict)


class CitizensData(BaseModel):
    count: int
    items: list[CitizenSummary]


class CitizenResponse(BaseModel):
    status: str
    message: str
    data: CitizenProfile


class ChronicleEvent(BaseModel):
    day: int
    title: str
    description: str
    before: dict[str, float | int]
    after: dict[str, float | int]
    event_impact: dict[str, float | int] = Field(default_factory=dict)
    daily_delta: dict[str, float | int] = Field(default_factory=dict)
    population_change: dict[str, Any] = Field(default_factory=dict)


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
