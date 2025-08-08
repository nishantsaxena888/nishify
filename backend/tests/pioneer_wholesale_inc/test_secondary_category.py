import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/secondary_category"

def test_create():
    payload = {
    "description": "political",
    "id": 9861,
    "name": "today"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/9861")
    assert response.status_code == 200

def test_update():
    payload = {
    "description": "political",
    "id": 9861,
    "name": "today"
}
    payload['id'] = 9861
    response = httpx.put(f"{BASE_URL}/9861", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/9861")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?description=political")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=9861")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=today")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=9860&id__lt=9862")
    assert response.status_code == 200