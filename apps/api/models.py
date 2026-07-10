from typing import Any

from pydantic import BaseModel, Field


class AgentModel(BaseModel):
    id: str
    name: str
    role: str
    age: int | None = None
    traits: list[str] = Field(default_factory=list)
    needs: dict[str, float] = Field(default_factory=dict)
    goals: list[str] = Field(default_factory=list)
    memories: list[dict[str, Any]] = Field(default_factory=list)
    relationships: dict[str, Any] = Field(default_factory=dict)


class AgentsResponse(BaseModel):
    count: int
    items: list[AgentModel]


class HistoryItem(BaseModel):
    day: int
    title: str
    deltas: dict[str, float | int] = Field(default_factory=dict)
    population: int | None = None
    cq: float | None = None


class HistoryResponse(BaseModel):
    count: int
    items: list[HistoryItem]


class WorldResponse(BaseModel):
    day: int = 0
    planet: str = ""
    city: str = ""
    population: int = 0
    energy: int | float = 0
    water: int | float = 0
    food: int | float = 0
    technology: int | float = 0
    cq: float = 0
    history: list[HistoryItem] = Field(default_factory=list)


class TickData(BaseModel):
    day: int
    world: WorldResponse
    agents: AgentsResponse


class TickResponse(BaseModel):
    status: str
    message: str
    data: TickData


class HealthResponse(BaseModel):
    name: str
    version: str
    status: str
