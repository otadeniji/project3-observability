from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_api_smoke(tmp_path, monkeypatch) -> None:
    database_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")
    client = TestClient(app)
    sample = Path("sample_logs/example_app.log").read_bytes()
    response = client.post("/api/logs/upload", files={"file": ("example_app.log", sample, "text/plain")})
    assert response.status_code == 200
    assert response.json()["imported"] == 14
    assert client.get("/api/health").json()["status"] == "healthy"
    assert client.get("/api/anomalies").status_code == 200
    assert client.get("/api/alerts").status_code == 200