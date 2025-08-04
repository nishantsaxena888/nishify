from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_item():
    payload = {   'active': True,
    'cash_discount_group_id': 5954,
    'category_id': 2935,
    'description': 'feel',
    'id': 9170,
    'item_code': 'government',
    'name': 'again',
    'price': 1987.59,
    'price_group_id': 2611,
    'secondary_category_id': 3646,
    'tax_group_id': 6737,
    'unit': 'star',
    'upc_code': 'yeah',
    'vendor_id': 2853}

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
