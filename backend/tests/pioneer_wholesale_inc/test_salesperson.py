import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/salesperson"

def test_create():
    payload = {
    "email": "fly",
    "id": 4995,
    "name": "shake",
    "phone": "in"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/4995")
    assert response.status_code == 200

def test_update():
    payload = {
    "email": "fly",
    "id": 4995,
    "name": "shake",
    "phone": "in"
}
    payload['id'] = 4995
    response = httpx.put(f"{BASE_URL}/4995", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/4995")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?email=fly")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=4995")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=shake")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?phone=in")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=4994&id__lt=4996")
    assert response.status_code == 200