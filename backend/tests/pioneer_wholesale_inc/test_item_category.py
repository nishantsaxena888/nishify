import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/item_category"

def test_create():
    payload = {
    "description": "evidence",
    "id": 6710,
    "name": "foot"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/6710")
    assert response.status_code == 200

def test_update():
    payload = {
    "description": "evidence",
    "id": 6710,
    "name": "foot"
}
    payload['id'] = 6710
    response = httpx.put(f"{BASE_URL}/6710", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/6710")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?description=evidence")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=6710")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=foot")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=6709&id__lt=6711")
    assert response.status_code == 200