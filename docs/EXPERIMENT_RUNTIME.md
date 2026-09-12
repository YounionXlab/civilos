# CivilOS Experiment Runtime

## Purpose

CivilOS is not only a civilization simulator. It is the runtime of the X-LAB Civilization Evolution Laboratory.

The experiment runtime connects:

1. a key evolution question,
2. a machine-readable experiment definition,
3. a deterministic civilization simulation,
4. structured observations,
5. and an experiment report.

For Alpha, keep this layer small. EXP-001 Ares Alpha remains the only active experiment.

## Runtime flow

```text
Experiment Definition
        ↓
Experiment Run
        ↓
Simulation Ticks
        ↓
Observations
        ↓
Experiment Report
```

## Canonical experiment definition

Experiment definitions live under:

```text
experiments/
```

Current experiment:

```text
experiments/exp-001-ares-alpha.json
```

An experiment definition should describe:

- experiment id
- title
- key question
- hypothesis
- world seed
- observation window
- metrics
- success signals
- failure signals

Experiment definitions do not mutate the world directly.

## Runtime package

Create the runtime under:

```text
packages/engine/experiments/
```

Recommended minimal modules:

```text
packages/engine/experiments/
    __init__.py
    loader.py
    run.py
    observation.py
    report.py
```

Do not introduce a framework or plugin system at this stage.

## ExperimentRun

A run is one execution of one experiment definition.

Minimum fields:

```text
run_id
experiment_id
world_seed
random_seed
started_sol
current_sol
observation_window
status
started_at
completed_at
```

Suggested status values:

```text
created
running
completed
failed
```

The runtime must not duplicate the civilization state. The existing World Engine remains the source of truth.

## Observations

An observation is a compact snapshot captured from the running civilization.

Minimum observation fields:

```text
run_id
experiment_id
sol
population
energy
water
food
technology
cq
citizen_health_mean
citizen_energy_mean
important_event_count
```

Alpha rule:

- record one observation per Sol,
- keep observations simple and structured,
- do not store full copies of every citizen every Sol.

## Experiment report

When a run reaches its observation window, generate a deterministic report.

The report should include:

### 1. Experiment

- id
- title
- key question
- hypothesis

### 2. Final state

- population
- energy
- water
- food
- technology
- CQ

### 3. Trend summary

For each main metric:

- start value
- end value
- minimum
- maximum
- average
- direction

### 4. Significant events

List the most important civilization events during the run.

### 5. Success / failure signals

Evaluate configured experiment signals where possible.

### 6. Result

Use one of:

```text
supported
partially_supported
not_supported
inconclusive
```

### 7. Insight

Generate a concise rule-based summary of what the run suggests.

Do not use an LLM for Alpha experiment conclusions.

## Architecture rule

The experiment runtime observes and coordinates the simulation.

It does not own civilization business logic.

Correct dependency direction:

```text
Experiment Runtime
        ↓
Simulation Engine
        ↓
World / Citizens
```

Incorrect:

```text
Simulation Engine
        ↓
Experiment Runtime
```

The Simulation Engine must remain usable without experiments enabled.

## EXP-001 milestone

EXP-001 Ares Alpha should be able to:

1. load its experiment definition,
2. create a run,
3. advance one Sol using the existing Simulation Engine,
4. capture one observation,
5. repeat deterministically,
6. complete after 365 Sol,
7. generate a report.

## Acceptance criteria

- `exp-001-ares-alpha.json` can be loaded and validated.
- A run has a unique `run_id`.
- One simulation tick produces one experiment observation.
- Simulation code does not import experiment runtime code.
- A deterministic 365-Sol run can complete in tests.
- The same seed produces the same final experiment result.
- An experiment report is generated at completion.
- Existing API and dashboard behavior remain unchanged.

## Non-goals for Alpha

Do not add yet:

- multi-experiment orchestration,
- distributed simulation,
- user-authored experiments,
- experiment marketplace,
- LLM-generated conclusions,
- automatic scientific claims,
- automatic policy recommendations.

The Alpha goal is smaller:

> Prove that one civilization experiment can run, be observed, and produce a reproducible report.
