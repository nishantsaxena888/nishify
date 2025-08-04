from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_invoice():
    payload = {   'customer_id': 2933,
    'date': datetime.datetime(2025, 7, 3, 14, 56, 9),
    'id': 6210,
    'status': 'task'}

    response = client.post("/api/invoice", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_invoice():
    response = client.get("/api/invoice")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_invoice_options():
    response = client.get("/api/invoice/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
