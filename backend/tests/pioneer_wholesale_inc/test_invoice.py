import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/invoice"

def test_create():
    payload = {
    "customer_id": 2933,
    "date": "2025-07-03T14:56:09",
    "id": 6210,
    "status": "task"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/6210")
    assert response.status_code == 200

def test_update():
    payload = {
    "customer_id": 2933,
    "date": "2025-07-03T14:56:09",
    "id": 6210,
    "status": "task"
}
    payload['id'] = 6210
    response = httpx.put(f"{BASE_URL}/6210", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/6210")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?customer_id=2933")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=6210")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?status=task")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?customer_id__gt=2932&customer_id__lt=2934")
    assert response.status_code == 200