from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from statistics import mean
from typing import Any

from .run import ExperimentRun

CORE_METRICS = ("population", "energy", "water", "food", "technology", "cq")


@dataclass(frozen=True)
class ExperimentReport:
    experiment: dict[str, Any]
    final_state: dict[str, float | int]
    metrics: dict[str, dict[str, float | int | str]]
    significant_events: list[dict[str, Any]]
    success_signals: list[dict[str, Any]]
    failure_signals: list[dict[str, Any]]
    result: str
    insight: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _metric_summary(values: list[float | int]) -> dict[str, float | int | str]:
    start = values[0]
    end = values[-1]
    if end > start:
        direction = "up"
    elif end < start:
        direction = "down"
    else:
        direction = "flat"
    return {
        "start": start,
        "end": end,
        "min": min(values),
        "max": max(values),
        "average": round(mean(values), 4),
        "direction": direction,
    }


def _event_summary(run: ExperimentRun) -> list[dict[str, Any]]:
    counts = Counter(event.get("title", "Untitled event") for event in run.events)
    return [
        {"title": title, "count": count}
        for title, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def _evaluate_signals(run: ExperimentRun) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    observations = run.observations
    min_resource = min(
        min(getattr(obs, resource) for obs in observations)
        for resource in ("energy", "water", "food")
    )
    viable = observations[-1].population > 0 and min_resource > 0
    differentiated = len({agent.get("profession") for agent in run.agents}) > 1
    memories_present = any(agent.get("memories") for agent in run.agents)
    event_traces = bool(run.events) and memories_present
    recovered = any(
        getattr(observations[index], resource) > getattr(observations[index - 1], resource)
        for resource in ("energy", "water", "food")
        for index in range(1, len(observations))
    )
    deterministic_consistency = True

    success_flags = [viable, differentiated, event_traces, recovered, bool(run.events)]
    failure_flags = [not viable, False, not differentiated, False, not deterministic_consistency]

    success = [
        {"signal": signal, "met": success_flags[index] if index < len(success_flags) else False}
        for index, signal in enumerate(run.experiment.get("success_signals", []))
    ]
    failure = [
        {"signal": signal, "met": failure_flags[index] if index < len(failure_flags) else False}
        for index, signal in enumerate(run.experiment.get("failure_signals", []))
    ]
    return success, failure


def _result(success: list[dict[str, Any]], failure: list[dict[str, Any]]) -> str:
    failures_met = sum(bool(item["met"]) for item in failure)
    successes_met = sum(bool(item["met"]) for item in success)
    if failures_met >= 2:
        return "not_supported"
    if successes_met == len(success) and failures_met == 0:
        return "supported"
    if successes_met > 0 and failures_met <= 1:
        return "partially_supported"
    return "inconclusive"


def _insight(result: str, metrics: dict[str, dict[str, float | int | str]]) -> str:
    resource_floor = min(float(metrics[key]["min"]) for key in ("energy", "water", "food"))
    tech_delta = float(metrics["technology"]["end"]) - float(metrics["technology"]["start"])
    cq_delta = float(metrics["cq"]["end"]) - float(metrics["cq"]["start"])
    if result == "supported":
        return (
            f"Ares Alpha remained viable across the observation window with a resource floor of {resource_floor:.2f}; "
            f"technology changed by {tech_delta:.2f} and CQ by {cq_delta:.2f}, supporting the hypothesis that material resilience and coordinated capability can reinforce one another."
        )
    if result == "partially_supported":
        return (
            f"Ares Alpha produced mixed evidence: the colony retained at least partial viability, with a resource floor of {resource_floor:.2f}, "
            f"while technology changed by {tech_delta:.2f} and CQ by {cq_delta:.2f}. The hypothesis requires further comparison runs."
        )
    if result == "not_supported":
        return (
            f"Ares Alpha failed one or more core viability conditions; the minimum resource level reached {resource_floor:.2f}. "
            "The current hypothesis is not supported under these initial conditions."
        )
    return "The run did not produce enough rule-based evidence to evaluate the hypothesis conclusively."


def generate_report(run: ExperimentRun) -> ExperimentReport:
    if run.status != "completed" or not run.observations:
        raise RuntimeError("A completed experiment run is required to generate a report")

    metrics: dict[str, dict[str, float | int | str]] = {}
    for key in CORE_METRICS:
        values = [getattr(observation, key) for observation in run.observations]
        metrics[key] = _metric_summary(values)

    final = run.observations[-1]
    final_state = {key: getattr(final, key) for key in CORE_METRICS}
    success, failure = _evaluate_signals(run)
    result = _result(success, failure)
    experiment_metadata = {
        "id": run.experiment["id"],
        "title": run.experiment["title"],
        "questions": list(run.experiment.get("questions", [])),
        "hypothesis": run.experiment["hypothesis"],
        "world_seed": run.experiment.get("world_seed"),
        "random_seed": run.experiment.get("random_seed"),
        "observation_window": dict(run.experiment["observation_window"]),
    }
    return ExperimentReport(
        experiment=experiment_metadata,
        final_state=final_state,
        metrics=metrics,
        significant_events=_event_summary(run),
        success_signals=success,
        failure_signals=failure,
        result=result,
        insight=_insight(result, metrics),
    )
