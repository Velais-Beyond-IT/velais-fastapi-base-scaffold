from datetime import datetime

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    # Verify timestamp is in ISO format
    datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
