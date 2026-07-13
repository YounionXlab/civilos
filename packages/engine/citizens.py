from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Memory:
    day: int
    type: str
    description: str
    impact: str


@dataclass
class Relationship:
    type: str
    strength: float

    def __post_init__(self) -> None:
        if not 0 <= self.strength <= 1:
            raise ValueError("Relationship strength must be between 0 and 1")


@dataclass
class Citizen:
    id: str
    name: str
    aliases: list[str]
    age: int
    gender: str
    birth_sol: int
    profession: str
    skills: list[str]
    traits: list[str]
    personality: str
    goal: str
    mood: str
    energy: int
    health: int
    current_task: str
    memories: list[Memory] = field(default_factory=list)
    relationships: dict[str, Relationship] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id or not self.name:
            raise ValueError("Citizen id and name are required")
        if self.age < 0 or self.birth_sol < 0:
            raise ValueError("Citizen age and birth_sol cannot be negative")
        if not 0 <= self.energy <= 100 or not 0 <= self.health <= 100:
            raise ValueError("Citizen energy and health must be between 0 and 100")

    @property
    def latest_memory(self) -> Memory | None:
        return self.memories[-1] if self.memories else None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Citizen":
        return cls(
            id=data["id"],
            name=data["name"],
            aliases=list(data.get("aliases", [])),
            age=int(data.get("age", 30)),
            gender=data.get("gender", "unspecified"),
            birth_sol=int(data.get("birth_sol", 0)),
            profession=data.get("profession", "Citizen"),
            skills=list(data.get("skills", [])),
            traits=list(data.get("traits", [])),
            personality=data.get("personality", "adaptable"),
            goal=data.get("goal", "Support the colony"),
            mood=data.get("mood", "steady"),
            energy=int(data.get("energy", 70)),
            health=int(data.get("health", 90)),
            current_task=data.get("current_task", "Review daily priorities"),
            memories=[Memory(**memory) for memory in data.get("memories", [])],
            relationships={
                citizen_id: Relationship(**relationship)
                for citizen_id, relationship in data.get("relationships", {}).items()
            },
        )
