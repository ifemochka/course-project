from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestSecurityControls:
    def test_input_validation_long_title(self):
        """Негативный тест: заголовок > 200 символов"""
        response = client.post(
            "/suggestions",
            json={
                "title": "A" * 201,
                "user_id": "user-123",
            },
        )
        assert response.status_code == 422
        assert response.headers["content-type"] == "application/problem+json"

    def test_input_validation_empty_user_id(self):
        """Негативный тест: пустой user_id"""
        response = client.post(
            "/suggestions",
            json={
                "title": "Test",
                "user_id": "   ",
            },
        )
        assert response.status_code == 422

    def test_problem_detail_format(self):
        """Позитивный тест: формат ошибок RFC 7807"""
        response = client.get("/suggestions/999999")
        assert response.status_code == 404
        data = response.json()
        assert "type" in data
        assert "title" in data
        assert "status" in data
        assert "correlation_id" in data

    def test_sql_injection_protection(self):
        """Негативный тест: защита от SQL injection"""
        response = client.get("/suggestions?user_id=test' OR '1'='1")
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            data = response.json()
            assert len(data) == 0 or all(
                "test" in str(item.get("user_id", "")) for item in data
            )

    def test_whitespace_trimming(self):
        """Тест автоматического триммирования пробелов"""
        response = client.post(
            "/suggestions",
            json={
                "title": "  Test Title  ",
                "user_id": "  user-123  ",
            },
        )
        if response.status_code == 200:
            data = response.json()
            assert data["title"] == "Test Title"
            assert data["user_id"] == "user-123"
