from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_item():
    payload = {   'active': False,
    'cash_discount_group_id': 496,
    'category_id': 4032,
    'description': 'choice',
    'id': 1671,
    'item_code': 'how',
    'name': 'field',
    'price': 3319.0,
    'price_group_id': 5824,
    'secondary_category_id': 2424,
    'tax_group_id': 1212,
    'unit': 'get',
    'upc_code': 'fire',
    'vendor_id': 1408}

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
