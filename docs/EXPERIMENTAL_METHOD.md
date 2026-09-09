# X-LAB Experimental Method

## Purpose

X-LAB uses one shared experimental grammar across civilization, society, climate, biology, materials, energy, and space research while allowing each domain to keep its own scientific methods.

The common chain is:

```text
Question
→ Prior Evidence
→ Hypothesis
→ Study Design
→ Variables / Controls
→ Protocol
→ Measurement
→ Run / Sample
→ Analysis
→ Robustness / Replication
→ Result
→ Insight
→ Reality Feedback
```

The goal is not to force every domain into one model. The goal is to make evidence, assumptions, quality, and uncertainty traceable.

---

## Canonical Experiment Types

X-LAB recognizes the following shared experiment / study types.

### Observation
Observe a system without deliberately changing the independent variable.

Examples: longitudinal observation, cohort, time series, natural experiment, ecological observation.

### Comparison
Compare two or more groups, systems, policies, configurations, or time periods.

### Intervention
Deliberately change one or more independent variables and measure outcomes.

### Factorial
Vary multiple factors systematically to estimate main effects and interactions.

### Sensitivity
Measure how strongly outputs change when inputs or assumptions change.

### Stress
Push a system away from normal operating conditions and measure resilience and recovery.

### Boundary
Search for a failure threshold, phase transition, tipping point, or breaking condition.

### Replication
Repeat an existing experiment or analysis to test repeatability or reproducibility.

### Ablation
Remove a mechanism, component, institution, variable, or model feature to estimate its contribution.

### Monte Carlo
Repeat a model or stochastic process across many seeds / samples to estimate a result distribution rather than one trajectory.

A single research program may use several types in sequence.

---

## Experimental Quality Dimensions

Every substantial experiment should be evaluated on ten quality dimensions.

1. **Question clarity** — Is the research question specific and decision-relevant?
2. **Falsifiability** — Can the hypothesis be contradicted by observable results?
3. **Control quality** — Is there an appropriate baseline / control / counterfactual?
4. **Variable isolation** — Are independent variables separated from confounders where possible?
5. **Sample size / repetitions** — Is there enough data, subjects, runs, or seeds?
6. **Measurement validity** — Do the metrics measure what they claim to measure?
7. **Statistical / analytical rigor** — Is the analysis appropriate and declared before interpretation?
8. **Reproducibility** — Can another researcher rerun the work from preserved inputs, versions, code, and data?
9. **Robustness / sensitivity** — Does the result survive alternate assumptions, stress tests, and perturbations?
10. **External validity** — How far can the result be generalized beyond the model, sample, or laboratory context?

### Experiment Quality Score (EQS)

X-LAB may summarize these ten dimensions as a 0–100 Experiment Quality Score.

Recommended default weighting:

```text
question_clarity             10
falsifiability               10
control_quality              10
variable_isolation           10
sample_size_repetitions      10
measurement_validity         10
analysis_rigor               10
reproducibility              10
robustness_sensitivity       10
external_validity            10
```

EQS is a compact audit signal, not a replacement for domain-specific peer review.

---

## Evidence Levels

X-LAB distinguishes evidence strength from confidence wording.

```text
E0  Idea / hypothesis only
E1  Single model or single observational indication
E2  Repeated or comparative evidence inside one model / dataset family
E3  Cross-model, cross-dataset, or independent replication evidence
E4  Empirical real-world evidence with credible causal or predictive support
E5  Broad multi-source replication / strong external validation
```

Simulation-derived insight must never be described as real-world validated merely because its internal run confidence is high.

Recommended interpretation fields:

```text
model_evidence
experimental_inference
real_world_implication
```

---

## Minimum Experiment Definition

A high-quality experiment should record, where applicable:

- experiment ID;
- research question IDs;
- prior evidence references;
- hypothesis;
- study type;
- control / baseline;
- independent variables;
- dependent variables;
- known confounders;
- sample / run / seed strategy;
- randomization strategy;
- measurement definitions;
- protocol;
- analysis plan;
- success / failure criteria;
- robustness and sensitivity plan;
- replication plan;
- expected limitations.

Not every field is relevant to every domain, but omitted fields should be intentionally omitted rather than silently assumed.

---

## Preregistration Principle

Where feasible, X-LAB should freeze the following before executing the decisive run or collecting the decisive data:

- hypothesis;
- primary outcomes;
- intervention / comparison design;
- exclusion rules;
- analysis plan;
- success / failure criteria.

Exploratory analysis is allowed, but it must be labeled exploratory rather than retroactively presented as preregistered confirmation.

---

## Reproducibility Contract

A reproducible X-LAB experiment should preserve:

```text
Experiment Definition
Data / Dataset Version
Code / Runtime Version
Model Version
Initial Conditions
Parameters
Random Seed(s)
Protocol
Analysis Script / Logic
Outputs
Environment / Dependency Version
```

For simulation experiments, one deterministic run is a trajectory, not a population-level conclusion. Stronger inference normally requires scenario comparison, multiple seeds, sensitivity tests, or independent models.

---

## Public Evidence Layer

X-LAB should use external public evidence when it can materially improve model assumptions, validation, or real-world relevance.

Examples of public sources include:

- ClinicalTrials.gov — clinical study registry and results metadata;
- GEO / GenBank — genomics and sequence data;
- OpenNeuro — neuroimaging and electrophysiology datasets;
- ICPSR — social and behavioral science datasets;
- PANGAEA — Earth and environmental science data;
- GBIF — biodiversity occurrence data;
- Dryad — cross-disciplinary research datasets;
- Zenodo — general open research datasets, software, and artifacts.

These sources are inputs to an Evidence Layer, not automatic truth. Source provenance, version, license, scope, and methodological limitations must remain traceable.

---

## Experiment Lifecycle

Recommended lifecycle:

```text
DRAFT
  ↓
PREREGISTERED / PLANNED
  ↓
RUNNING
  ↓
COMPLETED
  ↓
REVIEWED
  ↓
REPLICATED / CONTESTED / SUPERSEDED
```

The corresponding insight lifecycle remains separate. Completing an experiment does not automatically validate an insight.

---

## Design Rule

The standard for an excellent X-LAB experiment is not "did it produce an interesting result?"

It is:

> Was the question clear, the hypothesis falsifiable, the intervention or comparison controlled, the measurement valid, the result reproducible, the uncertainty visible, and the inference proportional to the evidence?
