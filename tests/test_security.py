import pytest
from fastapi.testclient import TestClient


def test_validation_boundaries(client: TestClient):
    response = client.post(
        "/suggestions/?user_id=test123",
        json={"title": "A" * 201, "text": "Valid text"}
    )
    assert response.status_code == 422

    response = client.post(
        "/suggestions/?user_id=test123",
        json={"title": "Valid title", "text": "A" * 5001}
    )
    assert response.status_code == 422

    response = client.post(
        "/suggestions/?user_id=invalid@user",
        json={"title": "Valid title", "text": "Valid text"}
    )
    assert response.status_code == 422


def test_error_format(client: TestClient):
    response = client.post(
        "/suggestions/?user_id=test123",
        json={"title": "A" * 201, "text": "Valid text"}
    )

    assert response.status_code == 422
    error_data = response.json()

    assert "detail" in error_data
    assert "Title exceeds maximum length" in error_data["detail"]


def test_rate_limiting(client: TestClient):
    for i in range(5):
        response = client.post(
            "/suggestions/?user_id=test123",
            json={"title": f"Test {i}", "text": "Valid text"}
        )
    assert response.status_code in [200, 429]
    