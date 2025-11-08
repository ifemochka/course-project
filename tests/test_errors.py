from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_suggestion_not_found():
    response = client.get("/suggestions/999")
    assert response.status_code == 404


def test_suggestion_validation_error():
    response = client.post("/suggestions/", json={})
    assert response.status_code == 422
