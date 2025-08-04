from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_invoice_item():
    payload = {'invoice_id': 3129, 'item_id': 9831, 'price': 164.7, 'quantity': 9536}

    response = client.post("/api/invoice_item", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_invoice_item():
    response = client.get("/api/invoice_item")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_invoice_item_options():
    response = client.get("/api/invoice_item/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
