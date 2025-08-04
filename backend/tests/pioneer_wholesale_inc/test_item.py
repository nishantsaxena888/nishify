from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_item():
    payload = {   'active': True,
    'cash_discount_group_id': 2269,
    'category_id': 6199,
    'description': 'cause',
    'id': 9293,
    'item_code': 'million',
    'name': 'ground',
    'price': 7591.76,
    'price_group_id': 5765,
    'secondary_category_id': 79,
    'tax_group_id': 5371,
    'unit': 'southern',
    'upc_code': 'walk',
    'vendor_id': 5055}

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
