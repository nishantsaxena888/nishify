from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_vendor():
    payload = {   'address': 'gun',
    'contact_person': 'despite',
    'email': 'huge',
    'id': 8926,
    'name': 'gas',
    'phone': 'do'}

    response = client.post("/api/vendor", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_vendor():
    response = client.get("/api/vendor")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_vendor_options():
    response = client.get("/api/vendor/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
