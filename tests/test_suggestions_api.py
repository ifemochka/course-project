from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_suggestion():
    """Тест создания предложения"""
    response = client.post(
        "/suggestions/",
        params={"user_id": "test_user_123"},  # user_id в параметрах, а не в JSON
        json={"title": "Test Suggestion", "text": "This is a test suggestion"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Suggestion"
    assert data["status"] == "pending"
    assert data["user_id"] == "test_user_123"


def test_get_suggestions():
    """Тест получения списка предложений"""
    response = client.get("/suggestions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_suggestion_by_id():
    """Тест получения конкретного предложения"""
    create_response = client.post(
        "/suggestions/",
        params={"user_id": "test_user"},
        json={"title": "Test", "text": "Test content"},
    )
    assert create_response.status_code == 200
    suggestion_id = create_response.json()["id"]

    response = client.get(f"/suggestions/{suggestion_id}")
    assert response.status_code == 200
    assert response.json()["id"] == suggestion_id


def test_update_suggestion():
    """Тест обновления предложения"""
    create_response = client.post(
        "/suggestions/",
        params={"user_id": "test_user"},
        json={"title": "Original", "text": "Original text"},
    )
    assert create_response.status_code == 200
    suggestion_id = create_response.json()["id"]

    update_response = client.put(
        f"/suggestions/{suggestion_id}",
        json={"title": "Updated Title", "status": "approved"},
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "approved"


def test_delete_suggestion():
    """Тест удаления предложения"""
    create_response = client.post(
        "/suggestions/",
        params={"user_id": "test_user"},
        json={"title": "To Delete", "text": "Delete me"},
    )
    assert create_response.status_code == 200
    suggestion_id = create_response.json()["id"]

    delete_response = client.delete(f"/suggestions/{suggestion_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/suggestions/{suggestion_id}")
    assert get_response.status_code == 404
