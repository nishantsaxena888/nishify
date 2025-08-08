import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/price_group"

def test_create():
    payload = {
    "id": 9575,
    "markup_percent": 753.81,
    "name": "ten"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/9575")
    assert response.status_code == 200

def test_update():
    payload = {
    "id": 9575,
    "markup_percent": 753.81,
    "name": "ten"
}
    payload['id'] = 9575
    response = httpx.put(f"{BASE_URL}/9575", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/9575")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?id=9575")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?markup_percent=753.81")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=ten")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=9574&id__lt=9576")
    assert response.status_code == 200