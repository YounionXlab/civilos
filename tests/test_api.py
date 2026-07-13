from fastapi.testclient import TestClient

from apps.api.main import app
from packages.engine import storage


def seed_storage(tmp_path):
    (tmp_path / "world.json").write_text(
        """
        {
          "day": 1,
          "planet": "Mars",
          "city": "Ares Alpha",
          "population": 20,
          "energy": 82,
          "water": 77,
          "food": 91,
          "technology": 34,
          "cq": 0.42,
          "history": []
        }
        """,
        encoding="utf-8",
    )
    (tmp_path / "agents.json").write_text(
        """
        [
          {
            "id": "lin_yuan",
            "name": "Lin Yuan",
            "aliases": ["Lin"],
            "age": 31,
            "gender": "male",
            "birth_sol": 0,
            "profession": "Fusion Engineer",
            "skills": ["reactor calibration"],
            "traits": ["calm"],
            "personality": "analytical",
            "goal": "Upgrade Fusion Reactor",
            "mood": "focused",
            "energy": 80,
            "health": 95,
            "current_task": "Review reactor telemetry",
            "memories": [],
            "relationships": {}
          }
        ]
        """,
        encoding="utf-8",
    )


def test_read_routes_return_response_models(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    seed_storage(tmp_path)
    client = TestClient(app)

    world = client.get("/world")
    agents = client.get("/agents")
    history = client.get("/history")

    assert world.status_code == 200
    assert world.json()["data"]["city"] == "Ares Alpha"
    assert agents.status_code == 200
    assert agents.json()["data"]["count"] == 1
    assert agents.json()["data"]["items"][0]["latest_memory"] is None
    assert history.status_code == 200
    assert history.json()["data"] == {"count": 0, "items": []}


def test_tick_uses_consistent_response_schema_and_mutates_state(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    seed_storage(tmp_path)
    client = TestClient(app)

    response = client.post("/tick")
    payload = response.json()

    assert response.status_code == 200
    assert payload["status"] == "ok"
    assert payload["data"]["day"] == 2
    assert payload["data"]["world"]["day"] == 2
    assert payload["data"]["citizens"]["count"] == 1
    assert client.get("/world").json()["data"]["day"] == 2
    assert client.get("/history").json()["data"]["count"] == 1


def test_citizen_detail_route_returns_full_profile(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    seed_storage(tmp_path)
    client = TestClient(app)

    response = client.get("/agents/lin_yuan")

    assert response.status_code == 200
    assert response.json()["data"]["skills"] == ["reactor calibration"]
    assert response.json()["data"]["health"] == 95
    assert client.get("/agents/missing").status_code == 404
