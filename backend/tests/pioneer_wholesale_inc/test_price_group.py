import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/price_group"

def test_create():
    payload = {
    "id": 6714,
    "markup_percent": 3969.74,
    "name": "home"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/6714")
    assert response.status_code == 200

def test_update():
    payload = {
    "id": 6714,
    "markup_percent": 3969.74,
    "name": "home"
}
    payload['id'] = 6714
    response = httpx.put(f"{BASE_URL}/6714", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/6714")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?id=6714")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?markup_percent=3969.74")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=home")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=6713&id__lt=6715")
    assert response.status_code == 200