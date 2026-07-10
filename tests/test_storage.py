import json

import pytest

from packages.engine import storage
from packages.engine.storage import Storage, StorageError


def test_storage_load_returns_default_for_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)

    assert Storage.load("world", default={"day": 0}) == {"day": 0}


def test_storage_load_raises_for_invalid_json(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    (tmp_path / "world.json").write_text("{", encoding="utf-8")

    with pytest.raises(StorageError):
        Storage.load_world()


def test_storage_save_writes_json_atomically(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)

    Storage.save_world({"day": 2})

    assert json.loads((tmp_path / "world.json").read_text(encoding="utf-8")) == {"day": 2}
    assert not (tmp_path / "world.json.tmp").exists()
