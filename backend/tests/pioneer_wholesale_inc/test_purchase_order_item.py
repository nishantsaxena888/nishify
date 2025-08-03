from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_purchase_order_item():
    payload = {
    "po_id": 1,
    "item_id": 1,
    "quantity": 100,
    "unit_price": 1.05
}
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
