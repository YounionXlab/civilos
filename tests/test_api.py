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
            "role": "Fusion Engineer",
            "needs": {},
            "goals": [],
            "memories": []
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
    assert world.json()["city"] == "Ares Alpha"
    assert agents.status_code == 200
    assert agents.json()["count"] == 1
    assert history.status_code == 200
    assert history.json() == {"count": 0, "items": []}


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
    assert payload["data"]["agents"]["count"] == 1
    assert client.get("/world").json()["day"] == 2
