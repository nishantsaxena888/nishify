from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_purchase_order():
    payload = {   'date': datetime.datetime(2025, 2, 1, 17, 42, 52, 136624),
    'id': 3414,
    'status': 'democratic',
    'vendor_id': 7558}

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
