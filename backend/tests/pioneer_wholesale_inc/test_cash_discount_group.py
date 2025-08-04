from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_cash_discount_group():
    payload = {'discount_percent': 3176.9, 'id': 5015, 'name': 'wife', 'terms': 'charge'}

    response = client.post("/api/cash_discount_group", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_cash_discount_group():
    response = client.get("/api/cash_discount_group")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_cash_discount_group_options():
    response = client.get("/api/cash_discount_group/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
