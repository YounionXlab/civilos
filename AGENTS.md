# CivilOS AGENTS.md

## Mission
Build a living digital civilization. CivilOS is not a game; it is a civilization runtime.

## Current Milestone
Alpha 0.1 only. Do not add large new features until Alpha 0.1 is deployable on Vercel.

## Architecture
- `packages/engine/` owns world state, simulation, events, history, and storage.
- `apps/api/` exposes read/write HTTP APIs.
- `apps/web/` is a read-only Observation Deck that can trigger ticks.
- `data/` stores JSON state for the Alpha.

## Core Rules
1. One tick = one day.
2. Only the engine mutates civilization state.
3. The web app must not contain world logic.
4. Keep implementations simple and small.
5. Prefer data-driven behavior over hardcoded behavior.
6. Do not redesign architecture without explicit approval.

## Coding Guidelines
- Use clear names and small functions.
- Prefer type hints where practical.
- Avoid unnecessary dependencies.
- Keep modules focused and under roughly 300 lines when practical.
- Write tests when adding non-trivial logic.

## Git Workflow
- One feature per branch/PR.
- Keep commits small and focused.
- Commit message prefixes:
  - `feat(engine):`
  - `feat(api):`
  - `feat(web):`
  - `fix:`
  - `docs:`
  - `refactor:`

## API Surface for Alpha 0.1
- `GET /world`
- `GET /agents`
- `GET /history`
- `POST /tick`

## Definition of Done
A feature is done only if:
- it works,
- it does not break existing code,
- it is committed,
- and it moves us closer to a deployable Alpha.

## AI Developer Instruction
When implementing changes:
- read existing code first,
- reuse existing modules,
- keep the scope narrow,
- do not introduce new subsystems unless approved,
- complete the Alpha before expanding the vision.
