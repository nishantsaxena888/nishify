from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_inventory_location():
    payload = {'address': 'fight', 'id': 5313, 'name': 'send'}

    response = client.post("/api/inventory_location", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_inventory_location():
    response = client.get("/api/inventory_location")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_inventory_location_options():
    response = client.get("/api/inventory_location/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
