from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_suggestion():
    """Тест создания предложения"""
    response = client.post(
        "/suggestions/?user_id=test_user_123",
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
        "/suggestions/?user_id=test_user",
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
        "/suggestions/?user_id=test_user",
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
        "/suggestions/?user_id=test_user",
        json={"title": "To Delete", "text": "Delete me"},
    )
    assert create_response.status_code == 200
    suggestion_id = create_response.json()["id"]

    delete_response = client.delete(f"/suggestions/{suggestion_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/suggestions/{suggestion_id}")
    assert get_response.status_code == 404


def test_get_suggestions_filtered():
    """Тест фильтрации предложений по статусу"""
    client.post(
        "/suggestions/?user_id=test_user",
        json={"title": "Pending Suggestion", "text": "Pending content"},
    )

    response = client.get("/suggestions/?status=pending")
    assert response.status_code == 200
    suggestions = response.json()
    assert all(s["status"] == "pending" for s in suggestions)


def test_get_suggestion_not_found():
    """Тест получения несуществующего предложения - должно вернуть 404"""
    response = client.get("/suggestions/999")
    assert response.status_code == 404
    body = response.json()
    assert "error" in body
    assert body["error"]["code"] == "http_error"


def test_update_suggestion_not_found():
    """Тест обновления несуществующего предложения - должно вернуть 404"""
    response = client.put(
        "/suggestions/999", json={"title": "Updated", "status": "approved"}
    )
    assert response.status_code == 404
    body = response.json()
    assert "error" in body
    assert body["error"]["code"] == "http_error"


def test_delete_suggestion_not_found():
    """Тест удаления несуществующего предложения - должно вернуть 404"""
    response = client.delete("/suggestions/999")
    assert response.status_code == 404
    body = response.json()
    assert "error" in body
    assert body["error"]["code"] == "http_error"


def test_create_suggestion_validation_error():
    """Тест создания предложения с невалидными данными"""
    response = client.post(
        "/suggestions/", json={"title": "Test", "text": "Test content"}
    )
    assert response.status_code == 422
