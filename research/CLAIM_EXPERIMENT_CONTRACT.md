# CivilOS Research Claim–Experiment Contract v1.0

CivilOS experiments that participate in the X-LAB Research OS / Evolution Graph should move from topic-level association to explicit claim testing.

## Canonical chain

`Research Question -> Claim -> Experiment -> Run -> Result/Evidence -> Claim Update -> Insight`

## Minimum experiment contract

Each experiment should expose, directly or through a projection layer:

- `id` (`EXP-*`)
- `questionId` (`Q-*`)
- `claimId` (`CLM-*`)
- `status`
- `method`
- `primaryMetric`
- `supportCriterion`
- `challengeCriterion`
- `inconclusiveCriterion`
- `preregistrationId` or explicit preregistration status
- `limitations`

## Run and result separation

An experiment definition is not a result.

One experiment may have many runs. Each run should preserve:

- run ID
- experiment ID
- code/model/data version
- seed/configuration
- timestamps
- raw output references
- protocol deviations

A result/evidence object should then summarize one or more runs and declare its stance toward the tested claim:

- `supports_claim`
- `challenges_claim`
- `inconclusive_for`
- `context_for`

## Falsification rule

Before execution, the experiment must specify what observation would count against the claim. A design that only defines success evidence is exploratory, not falsification-oriented.

## Claim updates

Claim status or confidence must never be changed by a raw run automatically. Update only after an explicit synthesis step that records:

- evidence considered
- evidence excluded and why
- scope of the tested claim
- uncertainty
- reviewer/analysis provenance

## Scope rule

A result refuting a narrow operationalization does not automatically refute the broader research question.

## CivilOS-specific note

Simulation results are model evidence. They may test internal consistency, robustness or conditional implications of a claim, but they do not by themselves establish real-world empirical validity.
