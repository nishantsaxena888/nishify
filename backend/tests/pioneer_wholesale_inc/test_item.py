from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_item():
    payload = {   'active': True,
    'cash_discount_group_id': 5344,
    'category_id': 802,
    'description': 'new',
    'id': 5413,
    'item_code': 'finally',
    'name': 'machine',
    'price': 3834.98,
    'price_group_id': 733,
    'secondary_category_id': 3813,
    'tax_group_id': 4405,
    'unit': 'suggest',
    'upc_code': 'pattern',
    'vendor_id': 3292}

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
