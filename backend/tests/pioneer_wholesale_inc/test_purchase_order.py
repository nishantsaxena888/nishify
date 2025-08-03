from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_purchase_order():
    payload = {   'date': '2025-01-06T12:37:19.756205',
    'id': 3121,
    'status': 'describe',
    'vendor_id': 4114}

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
