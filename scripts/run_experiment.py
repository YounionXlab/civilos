from __future__ import annotations

import argparse
import json
from pathlib import Path

from packages.engine.experiments import generate_report, run_experiment


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the canonical CivilOS experiment and emit a JSON report.")
    parser.add_argument("--output", type=Path, default=None, help="Optional path to write the report JSON.")
    args = parser.parse_args()

    run = run_experiment()
    report = generate_report(run).to_dict()
    payload = {
        "run_id": run.run_id,
        "experiment_id": run.experiment_id,
        "status": run.status,
        "observations": len(run.observations),
        "report": report,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
