import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/cash_discount_group"

def test_create():
    payload = {
    "discount_percent": 421.6,
    "id": 534,
    "name": "industry",
    "terms": "international"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/534")
    assert response.status_code == 200

def test_update():
    payload = {
    "discount_percent": 421.6,
    "id": 534,
    "name": "industry",
    "terms": "international"
}
    payload['id'] = 534
    response = httpx.put(f"{BASE_URL}/534", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/534")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?discount_percent=421.6")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=534")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=industry")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?terms=international")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?discount_percent__gt=420.6&discount_percent__lt=422.6")
    assert response.status_code == 200