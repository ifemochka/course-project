from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_suggestion():
    response = client.post(
        "/suggestions", json={"title": "Test", "user_id": "user-123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"
    assert data["user_id"] == "user-123"


def test_get_suggestions():
    response = client.get("/suggestions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_suggestion_by_id():
    create_resp = client.post(
        "/suggestions", json={"title": "Test", "user_id": "user-123"}
    )
    suggestion_id = create_resp.json()["id"]

    response = client.get(f"/suggestions/{suggestion_id}")
    assert response.status_code == 200


def test_delete_suggestion():
    create_resp = client.post(
        "/suggestions", json={"title": "Test", "user_id": "user-123"}
    )
    suggestion_id = create_resp.json()["id"]

    response = client.delete(f"/suggestions/{suggestion_id}")
    assert response.status_code == 200
