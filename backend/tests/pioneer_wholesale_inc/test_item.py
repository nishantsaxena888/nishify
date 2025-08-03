from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_item():
    payload = {
    "id": 6112,
    "item_code": "last",
    "name": "experience",
    "category_id": 6580,
    "secondary_category_id": 1479,
    "vendor_id": 7254,
    "tax_group_id": 6528,
    "price_group_id": 6211,
    "cash_discount_group_id": 8511,
    "upc_code": "thus",
    "unit": "pass",
    "price": 6901.22,
    "description": "field",
    "active": true
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
