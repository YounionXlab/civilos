# X-LAB Evolution Architecture 2.0

## Mission

X-LAB is a human evolution laboratory.

It is not a single software product and not a collection of unrelated projects.

Its role is to identify important questions about human and civilization evolution, turn selected questions into models and experiments, explore alternate worlds and decisions, and bring useful insight back into reality.

The architecture has four major functional layers:

1. Research Agenda — define the questions worth studying.
2. Evolution Experiment System — turn questions into measurable experiments.
3. Possibility Systems — imagine, experience, and run alternate worlds.
4. Reality Decision System — convert insight into judgment and action.

---

## 1. Research Agenda — Human Evolution Key Questions

The Human Evolution Key Questions list is the canonical X-LAB research agenda.

It should contain questions such as:

- How can humanity respond better to flood, pandemic, conflict, and ecological crisis?
- How should human healthspan and cognition evolve?
- How do institutions remain adaptive under technological acceleration?
- How should humanity build its first cross-celestial civilization system?
- How can planetary and interplanetary governance mature alongside technology?

Each question should eventually have a canonical ID.

Example:

```text
Q-021
How should humanity build the first cross-celestial civilization system?
```

A question may map to multiple research tracks and multiple experiments.

---

## 2. Evolution Experiment System

The Evolution Experiment System is the shared experimental method used across different branches of the X-LAB technology tree.

The general grammar is:

```text
Question
  ↓
Variables
  ↓
Data
  ↓
Model
  ↓
State
  ↓
Metrics
  ↓
Scenario / Intervention
  ↓
Simulation / Experiment
  ↓
Observation
  ↓
Evaluation
  ↓
Feedback
```

This pattern can support domains such as:

- climate change;
- genetics and biological evolution;
- materials science;
- social development;
- civilization evolution;
- space expansion.

The shared layer should remain methodological first. Do not prematurely force all domains into one codebase.

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

## 3. Possibility Systems

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

---

## 4. Reality Decision System — YICE

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

YICE should not duplicate experimental-domain models. It consumes useful state, scenarios, and insight to improve real-world decisions.

---

## X-LAB Evolution Loop 2.0

The updated loop is:

```text
Reality
  ↓
Discover Key Question
  ↓
Imagine Possibility
  ↓
Experience Possibility
  ↓
Model / Run / Experiment Possibility
  ↓
Observation
  ↓
Insight
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
Fiction  → Imagine
Mirror   → Experience
CivilOS  → Run civilization possibilities
YICE     → Decide in reality
```

The Evolution Experiment System supports the modeling and measurement layer across multiple research branches.

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
EXP-CIV-001    Civilization
EXP-CLIMATE-001 Climate
EXP-BIO-001    Biology / Genetics
EXP-MAT-001    Materials
EXP-SOC-001    Society
EXP-SPACE-001  Space Expansion
EXP-ENERGY-001 Energy Systems
EXP-GOV-001    Governance
```

Existing legacy IDs can remain valid during migration.

---

## Design Principle

The architecture should guide product boundaries, not create bureaucracy.

Rules:

- Start from real questions.
- Build the smallest useful model.
- Measure what matters.
- Prefer reproducible experiments.
- Preserve domain-specific validation.
- Extract shared infrastructure only after repeated need is proven.
- Return insights to reality rather than treating simulation as an end in itself.

---

## Strategic Thesis

X-LAB is building a system for human evolution research in which important questions can move through a full cycle:

```text
Question
→ imagination
→ experience
→ modeling
→ experiment
→ observation
→ insight
→ decision
→ action
→ feedback
```

The long-term goal is not to predict every future.

It is to increase humanity's ability to explore possible futures, learn earlier, and make better choices before high-cost reality becomes the only experiment available.
