# Alpha 0.3-B Task Breakdown

## Backend

- [ ] Extend memory domain model and serialization defaults.
- [ ] Add stable chronicle event identifiers.
- [ ] Implement deterministic memory promotion, decay, and duplicate suppression.
- [ ] Extend relationship state with affinity, trust, familiarity, and last interaction day.
- [ ] Implement shared-event relationship updates.
- [ ] Add dangling-reference validation.
- [ ] Add deterministic behavior reasons influenced by memory and relationships.

## API

- [ ] Extend typed citizen profile responses.
- [ ] Preserve backward-compatible defaults for existing citizen data.
- [ ] Add validation and not-found/error coverage.

## Web

- [ ] Display behavior reason.
- [ ] Display important-memory timeline.
- [ ] Display relationship summaries and recent changes.
- [ ] Preserve existing loading, cancellation, and stale-request behavior.

## Validation

- [ ] Unit tests for memory lifecycle.
- [ ] Unit tests for positive and negative relationship changes.
- [ ] Tests for memory-driven and relationship-driven action selection.
- [ ] 100-day deterministic stability test.
- [ ] Web behavior tests.
- [ ] Python test suite passes.
- [ ] Next.js production build passes.
