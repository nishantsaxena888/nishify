import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/salesperson"

def test_create():
    payload = {
    "email": "finally",
    "id": 2979,
    "name": "reduce",
    "phone": "when"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/2979")
    assert response.status_code == 200

def test_update():
    payload = {
    "email": "finally",
    "id": 2979,
    "name": "reduce",
    "phone": "when"
}
    payload['id'] = 2979
    response = httpx.put(f"{BASE_URL}/2979", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/2979")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?email=finally")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=2979")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=reduce")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?phone=when")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=2978&id__lt=2980")
    assert response.status_code == 200