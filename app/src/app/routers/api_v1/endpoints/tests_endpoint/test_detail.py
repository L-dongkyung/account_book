from fastapi.testclient import TestClient

from main import app

test_client = TestClient(app)
test_client.post("/api/v1/user/", json={"email": "detail@test.com", "password": "secret"})
data = {"username": "detail@test.com", "password": "secret"}
token_response = test_client.post("/api/v1/login/access-token", data=data)
json_token = token_response.json()
header = {"Authorization": f"bearer {json_token.get('access_token')}"}

json_data = {
    "receipt_info": {
        "payment": 100,
        "store": "market",
        "memo": "food"
    },
    "detail_info": {
        "payment_method": "cark",
        "store_address": "bundang",
        "store_phone": "010-1234-1234",
        "store_info": "market"
    }
}
test_client.post("/api/v1/receipt/", json=json_data, headers=header)
response = test_client.get("/api/v1/receipt/", headers=header)
json_data = response.json()
receipt_id = json_data[0].get("id")
test_client.get(f"/api/v1/receipt/{receipt_id}/detail/", headers=header)
response = test_client.get(f"/api/v1/receipt/{receipt_id}/detail/", headers=header)
json_data = response.json()
detail_id = json_data[0].get("id")


def test_read_detail():
    global detail_id, header
    response = test_client.get(f"/api/v1/detail/{detail_id}", headers=header)
    assert response.status_code == 200

def test_copy_detail():
    global detail_id, header
    response = test_client.post(f"/api/v1/detail/{detail_id}", headers=header)
    assert response.status_code == 200