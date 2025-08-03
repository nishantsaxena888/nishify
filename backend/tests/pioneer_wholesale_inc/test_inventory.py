from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_inventory():
    payload = {'id': 8084, 'item_id': 7647, 'location_id': 9957, 'quantity': 7738}

    response = client.post("/api/inventory", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_inventory():
    response = client.get("/api/inventory")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_inventory_options():
    response = client.get("/api/inventory/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
