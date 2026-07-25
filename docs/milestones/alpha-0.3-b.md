# CivilOS Alpha 0.3-B: Citizen Memory & Relationships

## Objective

Turn citizens from typed state records into persistent, evolving actors whose meaningful memories and relationships influence deterministic behavior.

## Scope

### Structured memory lifecycle

- Add stable `event_id` links from citizen memories to chronicle events.
- Add memory category, emotional valence, importance, participants, and creation day.
- Distinguish short-term and long-term memories using deterministic promotion and decay rules.
- Merge or suppress low-value duplicate memories.
- Keep memory writes inside the Simulation Engine.

### Relationship Engine v0.1

- Expand relationships with affinity, trust, familiarity, and last interaction day.
- Update relationships through explicit shared-event participation.
- Positive cooperation raises trust and affinity.
- Conflict lowers affinity or trust.
- Inactivity may reduce familiarity within bounded deterministic rules.
- Reject dangling citizen references and maintain consistent serialization.

### Memory-driven behavior

- Let selected profession actions use relevant memories or relationships as deterministic inputs.
- Record a machine-readable `behavior_reason` explaining why a task was selected.
- Do not add LLMs, embeddings, vector databases, or nondeterministic social simulation.

### API and dashboard

- Return important memories, relationships, and behavior reasons in the citizen profile endpoint.
- Display an important-memory timeline, relationship list, and current-task explanation.
- Preserve existing dashboard visual language and Chronicle Export behavior.

## Definition of Done

- Every meaningful citizen memory references a valid chronicle event.
- At least two event classes deterministically change relationships.
- At least one profession action is influenced by memory and one by relationship state.
- Citizen profiles expose the new fields through typed API models.
- Dashboard explains the selected citizen's current behavior.
- A 100-day deterministic simulation completes without dangling relationship or memory references.
- Existing tests remain green and new backend/frontend behavior tests are added.
- Python tests, web behavior tests, and Next.js production build pass.

## Architecture constraints

- Only the Simulation Engine mutates world and citizen state.
- Behavior remains deterministic and reproducible.
- Storage remains compatible with existing Alpha data or includes an explicit migration/defaulting path.
- No AI/LLM integration in this milestone.
