import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/inventory"

def test_create():
    payload = {
    "id": 7671,
    "item_id": 6163,
    "location_id": 3616,
    "quantity": 8900
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/7671")
    assert response.status_code == 200

def test_update():
    payload = {
    "id": 7671,
    "item_id": 6163,
    "location_id": 3616,
    "quantity": 8900
}
    payload['id'] = 7671
    response = httpx.put(f"{BASE_URL}/7671", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/7671")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?id=7671")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?item_id=6163")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?location_id=3616")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?quantity=8900")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=7670&id__lt=7672")
    assert response.status_code == 200