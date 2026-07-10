import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


class StorageError(RuntimeError):
    pass


class Storage:
    @staticmethod
    def _path(name: str) -> Path:
        if not name.isidentifier():
            raise StorageError(f"Invalid storage name: {name}")
        return DATA_DIR / f"{name}.json"

    @staticmethod
    def load(name: str, default: Any = None) -> Any:
        path = Storage._path(name)
        if not path.exists():
            return default
        try:
            with path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except OSError as exc:
            raise StorageError(f"Unable to read storage file: {name}") from exc
        except json.JSONDecodeError as exc:
            raise StorageError(f"Storage file contains invalid JSON: {name}") from exc

    @staticmethod
    def save(name: str, data: Any) -> None:
        path = Storage._path(name)
        temporary_path = path.with_suffix(".json.tmp")
        try:
            DATA_DIR.mkdir(exist_ok=True)
            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.write("\n")
            temporary_path.replace(path)
        except (OSError, TypeError) as exc:
            raise StorageError(f"Unable to write storage file: {name}") from exc

    @staticmethod
    def load_world() -> dict[str, Any]:
        return Storage.load("world", default={})

    @staticmethod
    def save_world(world: dict[str, Any]) -> None:
        Storage.save("world", world)

    @staticmethod
    def load_agents() -> list[dict[str, Any]]:
        return Storage.load("agents", default=[])

    @staticmethod
    def save_agents(agents: list[dict[str, Any]]) -> None:
        Storage.save("agents", agents)
