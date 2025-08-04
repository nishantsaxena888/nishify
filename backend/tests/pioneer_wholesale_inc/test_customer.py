from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_customer():
    payload = {   'address': 'live',
    'credit_limit': 9667.39,
    'email': 'should',
    'id': 4140,
    'name': 'law',
    'phone': 'bad',
    'salesperson_id': 9132}

    response = client.post("/api/customer", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_customer():
    response = client.get("/api/customer")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_customer_options():
    response = client.get("/api/customer/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
