from __future__ import annotations

import json
from pathlib import Path

from packages.engine.experiments.scenarios import run_comparative_suite


def main() -> None:
    root = Path("results/exp-civ-001/comparative-001")
    root.mkdir(parents=True, exist_ok=True)
    suite = run_comparative_suite()
    for name, report in suite["reports"].items():
        (root / f"{name}.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    (root / "comparison.json").write_text(
        json.dumps(suite["comparison"], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(suite["comparison"], ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
