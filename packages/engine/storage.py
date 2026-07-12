import json
import os
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

BUNDLED_DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_DIR = BUNDLED_DATA_DIR
STATE_LOCK = threading.RLock()


class StorageError(RuntimeError):
    pass


class FileStateStore:
    def _path(self, name: str) -> Path:
        if not name.isidentifier():
            raise StorageError(f"Invalid storage name: {name}")
        return DATA_DIR / f"{name}.json"

    def load(self, name: str, default: Any = None) -> Any:
        path = self._path(name)
        if not path.exists():
            return default
        try:
            with path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except OSError as exc:
            raise StorageError(f"Unable to read storage file: {name}") from exc
        except json.JSONDecodeError as exc:
            raise StorageError(f"Storage file contains invalid JSON: {name}") from exc

    def save(self, name: str, data: Any) -> None:
        path = self._path(name)
        temporary_path = path.with_suffix(".json.tmp")
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.write("\n")
            temporary_path.replace(path)
        except (OSError, TypeError) as exc:
            raise StorageError(f"Unable to write storage file: {name}") from exc

    @contextmanager
    def transaction(self) -> Iterator[dict[str, Any]]:
        with STATE_LOCK:
            state = {
                "world": self.load("world", {}),
                "agents": self.load("agents", []),
            }
            yield state
            self.save("world", state["world"])
            self.save("agents", state["agents"])


class PostgresStateStore:
    def __init__(self, database_url: str):
        self.database_url = database_url

    def _connect(self):
        try:
            import psycopg
        except ImportError as exc:
            raise StorageError("Postgres storage requires psycopg") from exc
        return psycopg.connect(self.database_url)

    def _seed(self, name: str) -> Any:
        return FileStateStore().load(name, {} if name == "world" else [])

    def load(self, name: str, default: Any = None) -> Any:
        try:
            with self._connect() as connection, connection.cursor() as cursor:
                cursor.execute("SELECT payload FROM civilos_state WHERE name = %s", (name,))
                row = cursor.fetchone()
                return row[0] if row else default
        except Exception as exc:
            raise StorageError(f"Unable to read Postgres state: {name}") from exc

    def save(self, name: str, data: Any) -> None:
        try:
            with self._connect() as connection, connection.cursor() as cursor:
                self._upsert(cursor, name, data)
        except Exception as exc:
            raise StorageError(f"Unable to write Postgres state: {name}") from exc

    @staticmethod
    def _upsert(cursor, name: str, data: Any) -> None:
        cursor.execute(
            """
            INSERT INTO civilos_state (name, payload, updated_at)
            VALUES (%s, %s, now())
            ON CONFLICT (name) DO UPDATE
            SET payload = EXCLUDED.payload, updated_at = now()
            """,
            (name, json.dumps(data, ensure_ascii=False)),
        )

    @contextmanager
    def transaction(self) -> Iterator[dict[str, Any]]:
        try:
            with self._connect() as connection, connection.cursor() as cursor:
                cursor.execute("SELECT pg_advisory_xact_lock(%s)", (20260707,))
                state: dict[str, Any] = {}
                for name in ("world", "agents"):
                    cursor.execute(
                        "SELECT payload FROM civilos_state WHERE name = %s FOR UPDATE",
                        (name,),
                    )
                    row = cursor.fetchone()
                    state[name] = row[0] if row else self._seed(name)
                yield state
                self._upsert(cursor, "world", state["world"])
                self._upsert(cursor, "agents", state["agents"])
        except StorageError:
            raise
        except Exception as exc:
            raise StorageError("Unable to complete Postgres state transaction") from exc


def get_state_store():
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        return PostgresStateStore(database_url)
    if os.environ.get("VERCEL"):
        raise StorageError("DATABASE_URL is required for persistent Vercel storage")
    return FileStateStore()


class Storage:
    @staticmethod
    def load(name: str, default: Any = None) -> Any:
        return get_state_store().load(name, default)

    @staticmethod
    def save(name: str, data: Any) -> None:
        get_state_store().save(name, data)

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

    @staticmethod
    def transaction():
        return get_state_store().transaction()
