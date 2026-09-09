# X-LAB Research Data Contract

## Purpose

This document defines the canonical data flow connecting X-LAB research questions, external evidence, experiments, observations, reports, quality assessment, and insights.

The canonical chain is:

```text
Q-xxx
Research Question
    ↓
Prior Evidence / Evidence Sources
    ↓
EXP-xxx
Experiment Definition
    ↓
RUN-xxx
Experiment Run / Sample
    ↓
Observations
    ↓
Experiment Report
    ↓
Robustness / Replication / Quality Assessment
    ↓
INS-xxx
Research Insight
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
- `schemas/evidence_source.schema.json`

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

### Evidence Sources

Canonical registry:

`research/evidence_sources.json`

Evidence sources describe public or controlled external repositories, registries, archives, and knowledge bases that may inform experiment design, priors, calibration, or external validation.

Each source should preserve:

- stable source ID;
- name;
- domains;
- source type;
- access mode;
- canonical homepage;
- API availability where known;
- DOI support where relevant;
- limitations / notes.

External evidence is never automatically treated as verified truth. Provenance, version, methodology, scope, and license remain part of evidence quality.

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

Experiment definitions may additionally record methodological quality fields such as:

- study type;
- prior evidence references;
- control / baseline;
- independent variables;
- dependent variables;
- confounders;
- measurement definitions;
- analysis plan;
- robustness plan;
- replication plan;
- preregistration status;
- Experiment Quality Score (EQS) and quality dimensions.

The canonical shared experiment types are:

```text
observation
comparison
intervention
factorial
sensitivity
stress
boundary
replication
ablation
monte_carlo
```

See `docs/EXPERIMENTAL_METHOD.md` for the methodological contract.

---

### Experiment Runs

A run is a concrete execution of an experiment definition.

Recommended identifier:

`RUN-<experiment-id>-<sequence-or-hash>`

A run should preserve:

- experiment_id;
- run_id;
- schema_version;
- scenario / cohort / sample label where relevant;
- random seed or sample identity;
- exact initial conditions;
- runtime / model / code version;
- data / dataset version;
- start state;
- interventions;
- observation window;
- completion status.

Two runs may use the same experiment definition but different initial conditions, seeds, samples, or interventions.

---

### Observations

Observations are measurements, not conclusions.

They should capture values produced by the model or collected from the world at specific simulation states, time points, or sample indices.

Examples:

- resource values;
- citizen health;
- temperature;
- allele frequencies;
- material properties;
- social network measures.

Observations should remain domain-specific where necessary.

The shared contract is only that observations remain traceable to a run and timestamp / simulation step / sample.

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
- recovery behavior;
- sensitivity analysis;
- model limitations;
- quality assessment;
- provisional interpretation.

A report is not automatically an X-LAB Insight.

---

## Experiment Quality Score (EQS)

X-LAB may score substantial experiments on ten 0–10 dimensions, producing a 0–100 summary score:

```text
question_clarity
falsifiability
control_quality
variable_isolation
sample_size_repetitions
measurement_validity
analysis_rigor
reproducibility
robustness_sensitivity
external_validity
```

EQS is an audit aid, not a substitute for domain-specific scientific review.

---

## Evidence Levels

Insights may carry a shared evidence level:

```text
E0  Idea / hypothesis only
E1  Single model or single observational indication
E2  Repeated or comparative evidence inside one model / dataset family
E3  Cross-model, cross-dataset, or independent replication evidence
E4  Empirical real-world evidence with credible causal or predictive support
E5  Broad multi-source replication / strong external validation
```

Evidence level and confidence are related but not interchangeable.

A high-confidence deterministic simulation may still remain E1 or E2 if it lacks independent or empirical validation.

---

## Insight Promotion Rule

An `INS-xxx` object should only be created when there is explicit evidence supporting a reusable conclusion.

Do **not** create insights merely because an experiment completed.

An insight should record, where available:

- source questions;
- source experiments and/or runs;
- evidence level;
- experiment quality score;
- replication count;
- external datasets;
- model domains;
- model evidence;
- experimental inference;
- real-world implication;
- evidence;
- confidence;
- limitations;
- implications;
- decision relevance.

Recommended states:

```text
provisional
supported
contested
validated
superseded
```

Insight status should never be upgraded automatically from a successful run alone.

---

## No False Certainty

Simulation output is model evidence, not reality itself.

Every insight derived from simulation should preserve the distinction between:

1. model evidence;
2. experimental inference;
3. real-world implication.

A high-confidence simulation result can still have low real-world confidence when assumptions are weak or external validation is absent.

---

## Preregistration and Exploratory Analysis

Where feasible, decisive experiments should freeze before execution:

- hypothesis;
- primary outcomes;
- control / intervention design;
- exclusion rules;
- analysis plan;
- success / failure criteria.

Exploratory work is allowed and encouraged, but must be labeled exploratory rather than retroactively presented as confirmatory.

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
- every evidence source against the evidence source schema;
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

YICE should consume evidence-qualified insights rather than raw experiment state by default.

Preferred flow:

```text
External Evidence / Experiment
  ↓
Report
  ↓
Quality + Evidence Level
  ↓
Validated / Supported / Provisional Insight
  ↓
YICE World Model
  ↓
Decision / Strategy
```

Raw observations may still be available when deeper analysis is needed, but decision systems should retain source traceability and evidence strength.

---

## Current Implementation Direction

The research layer now supports:

1. canonical research questions and experiment mappings;
2. experiment schemas and runtime execution;
3. deterministic baseline and comparative scenario runs;
4. insight objects with explicit confidence and limitations;
5. a public Evidence Source registry;
6. shared experiment-type vocabulary;
7. optional EQS and evidence-level metadata;
8. CI validation of research data contracts.

The next scientific milestone is to use this structure for boundary, Monte Carlo, ablation, replication, and external-evidence experiments rather than increasing simulation complexity without validation.
