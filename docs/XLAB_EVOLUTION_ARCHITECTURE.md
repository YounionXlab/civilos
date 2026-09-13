# X-LAB Evolution Architecture 2.1

## Mission

X-LAB is a human evolution laboratory.

It is not a single software product and not a collection of unrelated projects.

Its role is to identify important questions about human and civilization evolution, connect those questions to prior evidence, turn selected questions into models and experiments, explore alternate worlds and decisions, and bring evidence-qualified insight back into reality.

The architecture has five major functional layers:

1. Research Agenda — define the questions worth studying.
2. Evidence Layer — connect public data, prior studies, external observations, and internal experimental history.
3. Evolution Experiment System — turn questions into measurable, reproducible experiments.
4. Possibility Systems — imagine, experience, and run alternate worlds.
5. Reality Decision System — convert evidence-qualified insight into judgment and action.

---

## 1. Research Agenda — Human Evolution Key Questions

The Human Evolution Key Questions list is the canonical X-LAB research agenda.

It should contain questions such as:

- How can humanity respond better to flood, pandemic, conflict, and ecological crisis?
- How should human healthspan and cognition evolve?
- How do institutions remain adaptive under technological acceleration?
- How should humanity build its first cross-celestial civilization system?
- How can planetary and interplanetary governance mature alongside technology?

Each question has a canonical ID and may map to multiple research tracks and experiments.

---

## 2. Evidence Layer

The Evidence Layer connects X-LAB experiments to knowledge that already exists.

It may include:

- public research databases;
- open datasets;
- trial registries;
- observational archives;
- published empirical findings;
- internal experiment reports;
- model calibration data;
- replication evidence.

Canonical public evidence sources are registered in:

`research/evidence_sources.json`

Examples include ClinicalTrials.gov, GEO, GenBank, OpenNeuro, ICPSR, PANGAEA, GBIF, Dryad, and Zenodo.

The Evidence Layer exists to prevent X-LAB from treating every question as if no prior evidence exists and to make external validation possible.

It does not turn imported data into truth automatically. Provenance, methodology, version, scope, and limitations remain first-class metadata.

---

## 3. Evolution Experiment System

The Evolution Experiment System is the shared experimental method used across different branches of the X-LAB technology tree.

The general grammar is:

```text
Question
  ↓
Prior Evidence
  ↓
Hypothesis
  ↓
Study Design
  ↓
Variables / Controls / Confounders
  ↓
Data / Model / State
  ↓
Metrics / Measurement
  ↓
Scenario / Intervention
  ↓
Simulation / Experiment
  ↓
Observation
  ↓
Analysis
  ↓
Robustness / Replication
  ↓
Quality Assessment
  ↓
Insight
```

This pattern can support domains such as:

- climate change;
- genetics and biological evolution;
- materials science;
- social development;
- civilization evolution;
- space expansion.

The shared layer should remain methodological first. Do not prematurely force all domains into one codebase.

### Shared Experiment Types

X-LAB uses a common vocabulary:

```text
Observation
Comparison
Intervention
Factorial
Sensitivity
Stress
Boundary
Replication
Ablation
Monte Carlo
```

These are methodological labels, not runtime implementations.

### Experiment Quality Score

Substantial experiments may be scored across ten 0–10 dimensions:

- question clarity;
- falsifiability;
- control quality;
- variable isolation;
- sample size / repetitions;
- measurement validity;
- analysis rigor;
- reproducibility;
- robustness / sensitivity;
- external validity.

The 0–100 summary is the Experiment Quality Score (EQS).

EQS is an audit aid, not a replacement for domain expertise or peer review.

### Candidate Domain Labs

```text
Evolution Experiment System
│
├── Climate Lab
├── Bio / Genetics Lab
├── Materials Lab
├── Society Lab
├── CivilOS — Civilization Evolution Runtime
└── Space Expansion Lab
```

Each lab owns its domain model, state variables, metrics, and validation methods.

---

## Evidence Levels

X-LAB distinguishes evidence strength from confidence language.

```text
E0  Idea / hypothesis only
E1  Single model or single observational indication
E2  Repeated or comparative evidence inside one model / dataset family
E3  Cross-model, cross-dataset, or independent replication evidence
E4  Empirical real-world evidence with credible causal or predictive support
E5  Broad multi-source replication / strong external validation
```

A simulation may have very high internal repeatability and still remain E1 or E2.

This protects the architecture from confusing model certainty with real-world validity.

---

## 4. Possibility Systems

X-LAB uses different products to explore possibility from different angles.

### Fiction / Multi-world Narratives — Imagine

Purpose:

> See what the world could become.

Fiction expands the search space of possible futures and creates high-level world hypotheses.

### Mirror Worlds / Interactive Experiences — Experience

Purpose:

> Experience choices and consequences personally.

Mirror Worlds place people inside a decision environment and let them feel tradeoffs, uncertainty, and consequence.

### CivilOS — Run

Purpose:

> Let a civilization-scale world continue operating over time.

CivilOS models population, resources, technology, institutions, governance, social coordination, culture, resilience, and long-term civilization dynamics.

CivilOS is not the universal X-LAB experiment engine. It is the civilization-specific runtime within the broader Evolution Experiment System.

CivilOS results are model evidence until they are compared with independent models or external empirical data.

---

## 5. Reality Decision System — YICE

YICE is the Human / Social World Model + Decision Engine.

Its role is to bring observation and experimental insight back into reality.

Its operating loop is:

```text
World State Estimation
  ↓
Trend / Future Prediction
  ↓
Positioning and Resource Layout
  ↓
Multi-agent Modeling
  ↓
Simulation
  ↓
Action
  ↓
Reality Feedback
```

In traditional YICE language:

```text
取势 → 布局 → 同人 → 推演 → 行动 → 反馈
```

YICE should not duplicate experimental-domain models. It consumes evidence-qualified state, scenarios, and insight to improve real-world decisions.

By default YICE should see, alongside an insight:

- evidence level;
- confidence;
- EQS where available;
- source experiments;
- external datasets;
- limitations;
- real-world applicability.

---

## X-LAB Evolution Loop 2.1

The updated loop is:

```text
Reality
  ↓
Discover Key Question
  ↓
Gather Prior Evidence
  ↓
Imagine Possibility
  ↓
Experience Possibility
  ↓
Model / Run / Experiment Possibility
  ↓
Observation
  ↓
Robustness / Replication / Quality Assessment
  ↓
Evidence-qualified Insight
  ↓
Real-world Decision
  ↓
Action
  ↓
Reality Feedback
  └────────────────────→ back to X-LAB
```

In product shorthand:

```text
Fiction   → Imagine
Mirror    → Experience
CivilOS   → Run civilization possibilities
Evidence  → Ground and validate
YICE      → Decide in reality
```

---

## Experimental Knowledge Graph

The long-term X-LAB research graph is:

```text
External Dataset / Prior Study
        ↓
Research Question
        ↓
Hypothesis
        ↓
Experiment Definition
        ↓
Experiment Run / Sample
        ↓
Observation
        ↓
Report
        ↓
Replication / Robustness / Quality
        ↓
Insight
        ↓
YICE Decision
        ↓
Reality Feedback
```

This allows every insight to be traced backward to the exact evidence that produced it.

---

## Research Track Mapping

One key question can generate multiple experiments across different labs.

Example:

```text
Q-021
How should humanity build the first cross-celestial civilization system?

├── EXP-CIV-001
│   Ares Alpha
│   Civilization survival and evolution on Mars
│
├── EXP-SPACE-001
│   Cislunar Logistics
│   Transport and supply architecture
│
├── EXP-ENERGY-001
│   Lunar Power Grid
│   Energy generation, storage, and distribution
│
└── EXP-GOV-001
    Multi-planet Governance
    Governance under distance and communication delay
```

This structure prevents a single software product from being forced to solve every dimension of a research question.

---

## Experiment Naming

When multi-domain experiments become real, prefer domain-scoped experiment IDs.

Examples:

```text
EXP-CIV-001     Civilization
EXP-CLIMATE-001 Climate
EXP-BIO-001     Biology / Genetics
EXP-MAT-001     Materials
EXP-SOC-001     Society
EXP-SPACE-001   Space Expansion
EXP-ENERGY-001  Energy Systems
EXP-GOV-001     Governance
```

Existing legacy IDs can remain valid during migration.

---

## Design Principles

- Start from real questions.
- Search for existing evidence before inventing assumptions.
- Make hypotheses falsifiable.
- Preserve controls, confounders, and measurement definitions.
- Build the smallest useful model.
- Prefer reproducible experiments.
- Use multiple seeds / samples when making statistical claims.
- Distinguish exploratory analysis from confirmatory tests.
- Stress-test successful models and search for failure boundaries.
- Preserve domain-specific validation.
- Make evidence strength visible.
- Return insights to reality rather than treating simulation as an end in itself.

---

## Strategic Thesis

X-LAB is building an AI-native system for human evolution research in which important questions can move through a full cycle:

```text
Question
→ prior evidence
→ imagination
→ experience
→ modeling
→ experiment
→ observation
→ replication
→ quality assessment
→ insight
→ decision
→ action
→ feedback
```

The long-term goal is not to predict every future.

It is to increase humanity's ability to explore possible futures, distinguish strong evidence from weak evidence, learn earlier, and make better choices before high-cost reality becomes the only experiment available.
