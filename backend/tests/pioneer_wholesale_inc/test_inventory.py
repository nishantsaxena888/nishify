import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/inventory"

def test_create():
    payload = {
    "id": 1387,
    "item_id": 1299,
    "location_id": 9736,
    "quantity": 7122
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/1387")
    assert response.status_code == 200

def test_update():
    payload = {
    "id": 1387,
    "item_id": 1299,
    "location_id": 9736,
    "quantity": 7122
}
    payload['id'] = 1387
    response = httpx.put(f"{BASE_URL}/1387", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/1387")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?id=1387")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?item_id=1299")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?location_id=9736")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?quantity=7122")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=1386&id__lt=1388")
    assert response.status_code == 200