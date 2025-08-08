import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/state"

def test_create():
    payload = {
    "id": 9184,
    "name": "watch"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/9184")
    assert response.status_code == 200

def test_update():
    payload = {
    "id": 9184,
    "name": "watch"
}
    payload['id'] = 9184
    response = httpx.put(f"{BASE_URL}/9184", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/9184")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?id=9184")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=watch")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=9183&id__lt=9185")
    assert response.status_code == 200