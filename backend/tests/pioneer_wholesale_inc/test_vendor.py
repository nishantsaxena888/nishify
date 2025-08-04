from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_vendor():
    payload = {   'address': 'cell',
    'contact_person': 'relate',
    'email': 'kid',
    'id': 8614,
    'name': 'growth',
    'phone': 'middle'}

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
