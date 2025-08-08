import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/invoice"

def test_create():
    payload = {
    "customer_id": 249,
    "date": "2025-03-05T14:32:00.437808",
    "id": 7000,
    "status": "might"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/7000")
    assert response.status_code == 200

def test_update():
    payload = {
    "customer_id": 249,
    "date": "2025-03-05T14:32:00.437808",
    "id": 7000,
    "status": "might"
}
    payload['id'] = 7000
    response = httpx.put(f"{BASE_URL}/7000", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/7000")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?customer_id=249")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=7000")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?status=might")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?customer_id__gt=248&customer_id__lt=250")
    assert response.status_code == 200