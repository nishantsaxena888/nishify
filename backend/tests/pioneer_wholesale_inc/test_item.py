from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_item():
    payload = {   'active': False,
    'cash_discount_group_id': 8216,
    'category_id': 1295,
    'description': 'card',
    'id': 6066,
    'item_code': 'reflect',
    'name': 'either',
    'price': 6025.4,
    'price_group_id': 6825,
    'secondary_category_id': 5715,
    'tax_group_id': 6712,
    'unit': 'arm',
    'upc_code': 'card',
    'vendor_id': 9766}

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
