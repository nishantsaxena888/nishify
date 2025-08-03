from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_item():
    payload = {
    "active": false,
    "cash_discount_group_id": 8013,
    "category_id": 2884,
    "description": "increase",
    "id": 5559,
    "item_code": "each",
    "name": "only",
    "price": 2046.71,
    "price_group_id": 6962,
    "secondary_category_id": 6398,
    "tax_group_id": 7961,
    "unit": "history",
    "upc_code": "interesting",
    "vendor_id": 6100
}
    response = client.post("/api/item", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_item():
    response = client.get("/api/item")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_item_options():
    response = client.get("/api/item/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
