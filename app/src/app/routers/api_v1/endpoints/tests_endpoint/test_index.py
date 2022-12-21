from fastapi.testclient import TestClient

from main import app

test_client = TestClient(app)


def test_index():
    response = test_client.get("/api/v1/")
    response_text = response.text
    assert response_text[:len("fast api normal (UTC:")] == "fast api normal (UTC:"

def test_me_faild():
    response = test_client.get("/api/v1/me/", headers={"Authorization": "bearer asdf"})
    assert response.status_code == 403
    response = test_client.get("/api/v1/me/", headers={"Authorization": "asdf"})
    assert response.status_code == 401
