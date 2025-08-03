from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_item():
    payload = {   'active': True,
    'cash_discount_group_id': 161,
    'category_id': 5154,
    'description': 'dog',
    'id': 3164,
    'item_code': 'arrive',
    'name': 'since',
    'price': 3081.61,
    'price_group_id': 226,
    'secondary_category_id': 9421,
    'tax_group_id': 9953,
    'unit': 'Democrat',
    'upc_code': 'play',
    'vendor_id': 8117}

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
