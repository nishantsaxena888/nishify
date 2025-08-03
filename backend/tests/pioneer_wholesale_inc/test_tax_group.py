from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_tax_group():
    payload = {
    "id": 6891,
    "name": "far",
    "tax_percent": 1671.97
}
    response = client.post("/api/tax_group", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_tax_group():
    response = client.get("/api/tax_group")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_tax_group_options():
    response = client.get("/api/tax_group/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
