from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_item_category():
    payload = {'description': 'evidence', 'id': 6710, 'name': 'foot'}

    response = client.post("/api/item_category", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_item_category():
    response = client.get("/api/item_category")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_item_category_options():
    response = client.get("/api/item_category/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
