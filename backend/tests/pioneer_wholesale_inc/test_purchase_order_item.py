from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_purchase_order_item():
    payload = {'item_id': 8610, 'po_id': 5961, 'quantity': 4651, 'unit_price': 66.99}

    response = client.post("/api/purchase_order_item", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_purchase_order_item():
    response = client.get("/api/purchase_order_item")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_purchase_order_item_options():
    response = client.get("/api/purchase_order_item/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
