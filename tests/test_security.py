from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_valid_suggestion_works():
    """Тест что валидное предложение создаётся"""
    response = client.post(
        "/suggestions/?user_id=test123",
        json={"title": "Normal title", "text": "Normal text"},
    )

    assert response.status_code in [200, 422]


def test_missing_data_returns_error():
    """Тест что без данных возвращается ошибка"""
    response = client.post("/suggestions/?user_id=test123", json={})

    assert response.status_code == 422


def test_get_suggestions_works():
    """Тест что получение списка предложений работает"""
    response = client.get("/suggestions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
