import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/customer"

def test_create():
    payload = {
    "address": "party",
    "credit_limit": 3488.99,
    "email": "position",
    "id": 7094,
    "name": "more",
    "phone": "detail",
    "salesperson_id": 1753
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/7094")
    assert response.status_code == 200

def test_update():
    payload = {
    "address": "party",
    "credit_limit": 3488.99,
    "email": "position",
    "id": 7094,
    "name": "more",
    "phone": "detail",
    "salesperson_id": 1753
}
    payload['id'] = 7094
    response = httpx.put(f"{BASE_URL}/7094", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/7094")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?address=party")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?credit_limit=3488.99")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?email=position")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=7094")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=more")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?phone=detail")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?salesperson_id=1753")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?credit_limit__gt=3487.99&credit_limit__lt=3489.99")
    assert response.status_code == 200