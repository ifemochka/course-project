from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_not_found_item():
    r = client.get("/items/999")
    assert r.status_code == 404
    body = r.json()
    assert "title" in body and body["status"] == 404


def test_validation_error():
    r = client.post("/suggestions", json={"title": "", "user_id": "user-123"})
    assert r.status_code == 422
    body = r.json()
    assert "errors" in body


def test_suggestion_not_found():
    r = client.get("/suggestions/999")
    assert r.status_code == 404
    body = r.json()
    assert "title" in body and body["title"] == "Suggestion not found"
    assert "status" in body and body["status"] == 404
    assert "correlation_id" in body


def test_suggestion_validation_error():
    r = client.post("/suggestions/", json={})
    assert r.status_code == 422
    body = r.json()
    assert "errors" in body
