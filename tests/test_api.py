"""Tests for FastAPI endpoints."""

from fastapi.testclient import TestClient

from src.api.main import app


def test_health_endpoint() -> None:
    """Health endpoint should return ok."""
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
