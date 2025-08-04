import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/vendor"

def test_create():
    payload = {
    "address": "positive",
    "contact_person": "six",
    "email": "everyone",
    "id": 5420,
    "name": "social",
    "phone": "network",
    "state_id": 6081
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/5420")
    assert response.status_code == 200

def test_update():
    payload = {
    "address": "positive",
    "contact_person": "six",
    "email": "everyone",
    "id": 5420,
    "name": "social",
    "phone": "network",
    "state_id": 6081
}
    payload['id'] = 5420
    response = httpx.put(f"{BASE_URL}/5420", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/5420")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?address=positive")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?contact_person=six")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?email=everyone")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=5420")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=social")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?phone=network")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?state_id=6081")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=5419&id__lt=5421")
    assert response.status_code == 200