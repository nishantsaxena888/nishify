import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/purchase_order"

def test_create():
    payload = {
    "date": "2025-06-06T23:16:12.273522",
    "id": 4013,
    "status": "much",
    "vendor_id": 5546
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/4013")
    assert response.status_code == 200

def test_update():
    payload = {
    "date": "2025-06-06T23:16:12.273522",
    "id": 4013,
    "status": "much",
    "vendor_id": 5546
}
    payload['id'] = 4013
    response = httpx.put(f"{BASE_URL}/4013", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/4013")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?id=4013")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?status=much")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?vendor_id=5546")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=4012&id__lt=4014")
    assert response.status_code == 200