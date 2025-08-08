import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/customer"

def test_create():
    payload = {
    "address": "general",
    "credit_limit": 5139.36,
    "email": "present",
    "id": 999,
    "name": "class",
    "phone": "line",
    "salesperson_id": 1729
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/999")
    assert response.status_code == 200

def test_update():
    payload = {
    "address": "general",
    "credit_limit": 5139.36,
    "email": "present",
    "id": 999,
    "name": "class",
    "phone": "line",
    "salesperson_id": 1729
}
    payload['id'] = 999
    response = httpx.put(f"{BASE_URL}/999", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/999")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?address=general")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?credit_limit=5139.36")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?email=present")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=999")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=class")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?phone=line")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?salesperson_id=1729")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?credit_limit__gt=5138.36&credit_limit__lt=5140.36")
    assert response.status_code == 200