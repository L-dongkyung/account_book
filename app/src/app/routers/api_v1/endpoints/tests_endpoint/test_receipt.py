from fastapi.testclient import TestClient

from main import app

test_client = TestClient(app)
test_client.post("/api/v1/user/", json={"email": "receipt@test.com", "password": "secret"})
data = {"username": "receipt@test.com", "password": "secret"}
token_response = test_client.post("/api/v1/login/access-token", data=data)
json_token = token_response.json()
header = {"Authorization": f"bearer {json_token.get('access_token')}"}

receipt_id = 0


def test_create_receipt():
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
    response = test_client.post("/api/v1/receipt/", json=json_data, headers=header)
    assert response.status_code == 200


def test_list_receipt():
    global receipt_id
    response = test_client.get("/api/v1/receipt/", headers=header)
    assert response.status_code == 200
    json_data = response.json()
    receipt_id = json_data[0].get("id")


def test_update_receipt():
    global receipt_id
    json_data = {"payment": 1234, "memo": "test"}
    response = test_client.put(f"/api/v1/receipt/{receipt_id}", json=json_data, headers=header)
    assert response.status_code == 200


def test_get_detail():
    global receipt_id
    response = test_client.get(f"/api/v1/receipt/{receipt_id}/detail/", headers=header)
    assert response.status_code == 200


def test_delete_receipt():
    global receipt_id
    response = test_client.delete(f"/api/v1/receipt/{receipt_id}", headers=header)
    assert response.status_code == 200



