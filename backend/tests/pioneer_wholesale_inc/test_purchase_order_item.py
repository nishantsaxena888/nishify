from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_purchase_order_item():
    payload = {'item_id': 3911, 'po_id': 3124, 'quantity': 8981, 'unit_price': 4598.54}

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
