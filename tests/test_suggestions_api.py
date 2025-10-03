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
