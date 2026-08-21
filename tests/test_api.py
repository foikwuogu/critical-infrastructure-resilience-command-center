from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_health():
    assert client.get("/api/health").status_code==200

def test_resilience():
    r=client.get("/api/resilience")
    assert r.status_code==200
    assert 0<=r.json()["overall"]<=100

def test_assets():
    assert len(client.get("/api/assets").json())>=8

def test_scenario():
    r=client.post("/api/scenarios/bearing_degradation")
    assert r.status_code==200
    assert "change" in r.json()
