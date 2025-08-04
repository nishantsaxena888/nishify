from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_state():
    payload = {'id': 545, 'name': 'would'}

    response = client.post("/api/state", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_state():
    response = client.get("/api/state")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_state_options():
    response = client.get("/api/state/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
