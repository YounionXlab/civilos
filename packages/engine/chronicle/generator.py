from typing import Any, TypedDict


class JournalEntry(TypedDict):
    sol: int
    title: str
    opening: str
    citizens: list[str]
    citizen_story: str
    impact: str
    future_implication: str


def _latest_event(
    world: dict[str, Any],
    event: dict[str, Any] | None,
    history: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    if event:
        return event
    entries = history if history is not None else world.get("history", [])
    if not entries:
        raise ValueError("A chronicle event is required to generate a journal entry")
    return entries[-1]


def _citizens_involved(
    citizens: list[dict[str, Any]], event: dict[str, Any]
) -> list[dict[str, Any]]:
    event_text = f"{event.get('title', '')} {event.get('description', '')}".lower()
    named = [citizen for citizen in citizens if citizen["name"].lower() in event_text]
    if named:
        return named

    impact = event.get("event_impact", {})
    profession_keywords = {
        "energy": "fusion",
        "food": "botanist",
        "water": "water",
        "technology": "systems",
    }
    for resource in impact:
        keyword = profession_keywords.get(resource)
        if keyword:
            matched = [
                citizen
                for citizen in citizens
                if keyword in citizen.get("profession", "").lower()
            ]
            if matched:
                return matched[:1]

    if not citizens:
        return []
    sol = int(event.get("day", 0))
    return [citizens[(sol - 1) % len(citizens)]]


def _impact_story(event: dict[str, Any]) -> str:
    changes = event.get("daily_delta") or event.get("event_impact", {})
    meaningful = [(name, value) for name, value in changes.items() if value]
    if not meaningful:
        return "The colony absorbed the moment without a measurable change to its shared reserves."

    phrases = []
    for resource, value in meaningful:
        direction = "increased" if value > 0 else "decreased"
        amount = abs(value)
        display = int(amount) if amount == int(amount) else round(amount, 2)
        unit = "%" if resource != "population" else ""
        phrases.append(f"{resource.replace('_', ' ').title()} {direction} by {display}{unit}")
    return ", while ".join(phrases) + "."


def _future_implication(event: dict[str, Any]) -> str:
    impact = event.get("event_impact", {})
    if impact.get("technology", 0) > 0:
        return "The advance gives future crews a stronger foundation for the colony's next breakthrough."
    if impact.get("energy", 0) > 0:
        return "The additional power creates room for the colony to attempt more ambitious work tomorrow."
    if impact.get("water", 0) > 0 or impact.get("food", 0) > 0:
        return "Stronger reserves give the settlement more time to grow without compromising survival."
    if any(value < 0 for value in impact.values()):
        return "The setback will shape tomorrow's priorities as citizens work to restore the lost capacity."
    return "Citizens will carry the lesson from this sol into the decisions that follow."


def generate_journal_entry(
    world: dict[str, Any],
    citizens: list[dict[str, Any]],
    event: dict[str, Any] | None = None,
    history: list[dict[str, Any]] | None = None,
) -> JournalEntry:
    selected_event = _latest_event(world, event, history)
    involved = _citizens_involved(citizens, selected_event)
    names = [citizen["name"] for citizen in involved]
    if involved:
        citizen = involved[0]
        citizen_story = (
            f"{citizen['name']}, a {citizen['profession']}, helped carry the day's work through "
            f"by focusing on {citizen['current_task'].lower()}."
        )
    else:
        citizen_story = "The citizens of the colony worked together to carry the day forward."

    return {
        "sol": int(selected_event.get("day", world.get("day", 0))),
        "title": selected_event["title"].rstrip("."),
        "opening": selected_event.get(
            "description", "The colony reached another turning point in its shared story."
        ),
        "citizens": names,
        "citizen_story": citizen_story,
        "impact": _impact_story(selected_event),
        "future_implication": _future_implication(selected_event),
    }
