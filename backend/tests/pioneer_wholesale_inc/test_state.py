import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/state"

def test_create():
    payload = {
    "id": 7024,
    "name": "rock"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/7024")
    assert response.status_code == 200

def test_update():
    payload = {
    "id": 7024,
    "name": "rock"
}
    payload['id'] = 7024
    response = httpx.put(f"{BASE_URL}/7024", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/7024")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?id=7024")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=rock")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=7023&id__lt=7025")
    assert response.status_code == 200