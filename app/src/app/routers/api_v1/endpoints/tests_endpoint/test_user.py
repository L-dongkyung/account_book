from fastapi.testclient import TestClient

from main import app

test_client = TestClient(app)


def test_create_user():
    only_email_response = test_client.post("/api/v1/user/", json={"email": "test@test.com"})
    assert only_email_response.status_code == 422
    only_password_response = test_client.post("/api/v1/user/", json={"password": "secret"})
    assert only_password_response.status_code == 422
    created_response = test_client.post("/api/v1/user/", json={"email": "test@test.com", "password": "secret"})
    assert created_response.status_code == 200
    already_created_response = test_client.post("/api/v1/user/", json={"email": "test@test.com", "password": "secret"})
    assert already_created_response.status_code == 422


def test_delete_user():
    data = {"username": "test@test.com", "password": "secret"}
    token_response = test_client.post("/api/v1/login/access-token", data=data)
    json_token = token_response.json()
    response = test_client.delete("/api/v1/user/", headers={"Authorization": f"bearer {json_token.get('access_token')}"})
    assert response.status_code == 200
