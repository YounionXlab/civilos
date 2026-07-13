from dataclasses import dataclass


@dataclass(frozen=True)
class ProfessionAction:
    task: str
    resource_impact: dict[str, float]
    health_delta: int = 0


@dataclass(frozen=True)
class ProfessionBehavior:
    resource_impact: dict[str, float]
    tasks: tuple[str, ...]
    health_delta: int = 0

    def action_for(self, day: int, citizen_index: int) -> ProfessionAction:
        return ProfessionAction(
            task=self.tasks[(day + citizen_index) % len(self.tasks)],
            resource_impact=self.resource_impact,
            health_delta=self.health_delta,
        )


GENERIC_BEHAVIOR = ProfessionBehavior(
    resource_impact={},
    tasks=("Inspect shared systems", "Support colony operations", "Review daily priorities"),
)

PROFESSION_REGISTRY = {
    "fusion engineer": ProfessionBehavior(
        {"energy": 1.5, "technology": 0.05},
        ("Calibrate fusion controls", "Review reactor telemetry", "Inspect power conduits"),
    ),
    "botanist": ProfessionBehavior(
        {"food": 1.6, "water": 1.5},
        ("Monitor greenhouse crops", "Improve water efficiency", "Prepare the next harvest"),
    ),
    "miner": ProfessionBehavior(
        {"energy": 0.3, "technology": 0.06},
        ("Survey mineral seams", "Operate excavation equipment", "Catalog mineral samples"),
    ),
    "doctor": ProfessionBehavior(
        {},
        ("Review health reports", "Run wellness checks", "Prepare medical supplies"),
        health_delta=1,
    ),
    "researcher": ProfessionBehavior(
        {"technology": 0.15},
        ("Analyze experiment results", "Test a new material", "Document research findings"),
    ),
    "technician": ProfessionBehavior(
        {"energy": 0.4, "technology": 0.05},
        ("Repair habitat equipment", "Inspect sensor arrays", "Service colony robotics"),
    ),
    "teacher": ProfessionBehavior(
        {"technology": 0.08},
        ("Teach engineering fundamentals", "Lead a knowledge session", "Mentor a citizen"),
    ),
    "administrator": ProfessionBehavior(
        {"energy": 0.3, "water": 0.3, "food": 0.3},
        ("Coordinate daily priorities", "Review resource allocations", "Publish colony decisions"),
    ),
}


def behavior_for(profession: str) -> ProfessionBehavior:
    return PROFESSION_REGISTRY.get(profession.lower(), GENERIC_BEHAVIOR)
