from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_price_group():
    payload = {'id': 6714, 'markup_percent': 3969.74, 'name': 'home'}

    response = client.post("/api/price_group", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_price_group():
    response = client.get("/api/price_group")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_price_group_options():
    response = client.get("/api/price_group/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
