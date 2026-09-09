# X-LAB Research Data Contract

## Purpose

This document defines the canonical data flow connecting X-LAB research questions, experiments, observations, reports, and insights.

The canonical chain is:

```text
Q-xxx
Research Question
    ↓
EXP-xxx
Experiment Definition
    ↓
RUN-xxx
Experiment Run
    ↓
Observations
    ↓
Experiment Report
    ↓
INS-xxx
Validated Insight
    ↓
YICE / Real-world Decision
    ↓
Reality Feedback
```

The goal is to ensure every X-LAB domain can share one interoperable research language without forcing every domain to use the same scientific model.

---

## Canonical Schemas

Current canonical schemas:

- `schemas/question.schema.json`
- `schemas/experiment.schema.json`
- `schemas/insight.schema.json`

Every machine-readable research object should validate against its corresponding schema before it is treated as canonical.

---

## Canonical Data Sources

### Questions

Canonical registry:

`research/questions.json`

A question should contain, at minimum:

- id;
- title;
- domain;
- priority;
- maturity;
- status.

Question identifiers are immutable once referenced by experiments or insights.

---

### Question–Experiment Mapping

Canonical mapping:

`research/mappings.json`

Mappings are many-to-many.

A question may generate multiple experiments, and an experiment may explore multiple research questions.

---

### Experiment Definitions

Canonical experiment definitions live under:

`experiments/`

Example:

`experiments/exp-001-ares-alpha.json`

New experiments should adopt domain-qualified identifiers where practical, for example:

- `EXP-CIV-001`
- `EXP-SPACE-001`
- `EXP-CLIMATE-001`
- `EXP-BIO-001`
- `EXP-MAT-001`
- `EXP-SOC-001`

The existing `EXP-001` identifier for Ares Alpha remains a compatibility alias during migration.

---

### Experiment Runs

A run is a concrete execution of an experiment definition.

Recommended identifier:

`RUN-<experiment-id>-<sequence-or-hash>`

A run should preserve:

- experiment_id;
- run_id;
- schema_version;
- random seed;
- exact initial conditions;
- runtime version;
- start state;
- observation window;
- completion status.

Two runs may use the same experiment definition but different initial conditions or interventions.

---

### Observations

Observations are measurements, not conclusions.

They should capture values produced by the model at specific simulation states or times.

Examples:

- resource values;
- citizen health;
- temperature;
- allele frequencies;
- material properties;
- social network measures.

Observations should remain domain-specific where necessary.

The shared contract is only that observations remain traceable to a run and timestamp / simulation step.

---

### Experiment Reports

Reports summarize one or more runs.

A report may contain:

- experiment metadata;
- run metadata;
- metric summaries;
- significant events;
- comparisons;
- uncertainty;
- success/failure signals;
- model limitations;
- provisional interpretation.

A report is not automatically an X-LAB Insight.

---

## Insight Promotion Rule

An `INS-xxx` object should only be created when there is explicit evidence supporting a reusable conclusion.

Do **not** create insights merely because an experiment completed.

An insight must record:

- source questions;
- source experiments and/or runs;
- evidence;
- confidence;
- limitations;
- implications;
- decision relevance.

Recommended states:

```text
draft
provisional
validated
superseded
retracted
```

The first Ares Alpha insight should therefore be created only after the initial 365-Sol experiment report exists.

---

## No False Certainty

Simulation output is model evidence, not reality itself.

Every insight derived from simulation should preserve the distinction between:

1. model behavior;
2. experimental inference;
3. real-world implication.

A high-confidence simulation result can still have low real-world confidence when assumptions are weak or external validation is absent.

---

## Versioning

Every canonical schema and major machine-readable object should include or inherit a schema version.

Recommended initial version:

`1.0.0`

Breaking changes should increment the major version.

Schema migration should preserve old identifiers and traceability.

---

## Validation Requirement

CI should validate:

- `research/questions.json` against the question schema;
- every canonical experiment definition against the experiment schema;
- every insight object against the insight schema;
- mapping references so that question and experiment IDs resolve;
- uniqueness of all canonical IDs;
- no dangling references.

Validation failure should fail CI.

---

## Architecture Boundary

The Research Data Contract must not force domain engines to share implementation logic.

Climate models, biological models, material simulations, society models, and CivilOS may use very different internal representations.

They only need to publish compatible research metadata and outputs at the contract boundary.

This preserves both scientific/domain flexibility and X-LAB-wide interoperability.

---

## Relationship to YICE

YICE should consume validated insights rather than raw experiment state by default.

Preferred flow:

```text
Experiment
  ↓
Report
  ↓
Validated / Provisional Insight
  ↓
YICE World Model
  ↓
Decision / Strategy
```

Raw observations may still be available when deeper analysis is needed, but decision systems should retain source traceability.

---

## Immediate Implementation Target

The next implementation milestone is:

1. validate all existing research JSON against schemas;
2. normalize Ares Alpha experiment metadata;
3. add reference integrity checks;
4. wire validation into tests and CI;
5. create the first `INS-xxx` only after EXP-CIV-001 completes a report-producing run.

This milestone should remain infrastructure-focused and must not introduce new simulation features.
