from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_suggestions_empty():
    """Тест получения пустого списка предложений"""
    response = client.get("/suggestions/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_suggestion_not_found():
    """Тест получения несуществующего предложения"""
    response = client.get("/suggestions/999")
    assert response.status_code == 404


def test_update_suggestion_not_found():
    """Тест обновления несуществующего предложения"""
    response = client.put("/suggestions/999", json={"title": "Test"})
    assert response.status_code == 404


def test_delete_suggestion_not_found():
    """Тест удаления несуществующего предложения"""
    response = client.delete("/suggestions/999")
    assert response.status_code == 404


def test_create_suggestion_missing_user_id():
    """Тест создания предложения без user_id"""
    response = client.post("/suggestions/", json={"title": "Test", "text": "Test"})
    assert response.status_code == 422


def test_create_and_get_suggestion():
    """Тест создания и получения предложения"""
    create_response = client.post(
        "/suggestions",
        json={"title": "Test Title", "text": "Test Description", "user_id": "user-123"},
    )
    assert create_response.status_code == 200

    list_response = client.get("/suggestions/")
    assert list_response.status_code == 200
    list_data = list_response.json()

    assert len(list_data) == 1
    assert list_data[0]["title"] == "Test Title"
    assert list_data[0]["user_id"] == "user-123"


def test_create_suggestion_with_whitespace():
    """Тест создания предложения с пробелами - проверка тримминга"""
    response = client.post(
        "/suggestions",
        json={
            "title": "  Test Title  ",
            "user_id": "  user-123  ",
            "text": "  test text  ",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Title"
    assert data["user_id"] == "user-123"
    assert data["text"] == "test text"
