from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_item():
    payload = {   'active': True,
    'cash_discount_group_id': 9624,
    'category_id': 8271,
    'description': 'southern',
    'id': 804,
    'item_code': 'affect',
    'name': 'four',
    'price': 9025.1,
    'price_group_id': 5428,
    'secondary_category_id': 9820,
    'tax_group_id': 9812,
    'unit': 'man',
    'upc_code': 'long',
    'vendor_id': 4902}

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
