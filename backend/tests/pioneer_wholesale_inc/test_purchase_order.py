from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_purchase_order():
    payload = {'date': None, 'id': 2583, 'status': 'media', 'vendor_id': 6443}

    response = client.post("/api/purchase_order", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_purchase_order():
    response = client.get("/api/purchase_order")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_purchase_order_options():
    response = client.get("/api/purchase_order/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
