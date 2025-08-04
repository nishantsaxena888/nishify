import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/cash_discount_group"

def test_create():
    payload = {
    "discount_percent": 633.18,
    "id": 2252,
    "name": "to",
    "terms": "travel"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/2252")
    assert response.status_code == 200

def test_update():
    payload = {
    "discount_percent": 633.18,
    "id": 2252,
    "name": "to",
    "terms": "travel"
}
    payload['id'] = 2252
    response = httpx.put(f"{BASE_URL}/2252", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/2252")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?discount_percent=633.18")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=2252")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=to")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?terms=travel")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?discount_percent__gt=632.18&discount_percent__lt=634.18")
    assert response.status_code == 200