from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_salesperson():
    payload = {'email': 'operation', 'id': 2012, 'name': 'bag', 'phone': 'same'}

    response = client.post("/api/salesperson", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_salesperson():
    response = client.get("/api/salesperson")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_salesperson_options():
    response = client.get("/api/salesperson/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
