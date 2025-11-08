from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_validation_long_title():
    response = client.post(
        "/suggestions", json={"title": "A" * 201, "user_id": "user-123"}
    )
    assert response.status_code == 422


def test_validation_empty_user():
    response = client.post("/suggestions", json={"title": "Test", "user_id": "   "})
    assert response.status_code == 422


def test_error_format():
    response = client.get("/suggestions/999")
    assert response.status_code == 404
    data = response.json()
    assert "title" in data
    assert "status" in data
