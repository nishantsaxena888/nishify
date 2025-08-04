import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/purchase_order"

def test_create():
    payload = {
    "date": "2025-02-08T04:04:37",
    "id": 5704,
    "status": "worry",
    "vendor_id": 5409
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/5704")
    assert response.status_code == 200

def test_update():
    payload = {
    "date": "2025-02-08T04:04:37",
    "id": 5704,
    "status": "worry",
    "vendor_id": 5409
}
    payload['id'] = 5704
    response = httpx.put(f"{BASE_URL}/5704", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/5704")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?id=5704")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?status=worry")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?vendor_id=5409")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=5703&id__lt=5705")
    assert response.status_code == 200