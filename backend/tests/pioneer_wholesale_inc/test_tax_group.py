import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/tax_group"

def test_create():
    payload = {
    "id": 6324,
    "name": "although",
    "tax_percent": 326.24
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/6324")
    assert response.status_code == 200

def test_update():
    payload = {
    "id": 6324,
    "name": "although",
    "tax_percent": 326.24
}
    payload['id'] = 6324
    response = httpx.put(f"{BASE_URL}/6324", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/6324")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?id=6324")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=although")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?tax_percent=326.24")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=6323&id__lt=6325")
    assert response.status_code == 200