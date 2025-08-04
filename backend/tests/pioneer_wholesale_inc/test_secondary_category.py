from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_secondary_category():
    payload = {'description': 'political', 'id': 657, 'name': 'bill'}

    response = client.post("/api/secondary_category", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_secondary_category():
    response = client.get("/api/secondary_category")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_secondary_category_options():
    response = client.get("/api/secondary_category/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
