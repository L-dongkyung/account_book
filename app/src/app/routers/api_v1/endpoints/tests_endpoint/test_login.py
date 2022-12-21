from fastapi.testclient import TestClient

from main import app

test_client = TestClient(app)


def test_access_token():
    created_response = test_client.post("/api/v1/user/", json={"email": "test@test.com", "password": "secret"})
    if created_response.status_code == 200:
        data = {"username":"test@test.com", "password": "secret"}
        token_response = test_client.post("/api/v1/login/access-token", data=data)
        json_token = token_response.json()
        user_response = test_client.get("/api/v1/me/", headers={"Authorization": f"bearer {json_token.get('access_token')}"})
        user = user_response.json()
        assert user.get("email") == "test@test.com"
        test_client.delete("/api/v1/user/", headers={"Authorization": f"bearer {json_token.get('access_token')}"})
