import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/item_category"

def test_create():
    payload = {
    "description": "top",
    "id": 1142,
    "name": "actually"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/1142")
    assert response.status_code == 200

def test_update():
    payload = {
    "description": "top",
    "id": 1142,
    "name": "actually"
}
    payload['id'] = 1142
    response = httpx.put(f"{BASE_URL}/1142", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/1142")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?description=top")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=1142")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=actually")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=1141&id__lt=1143")
    assert response.status_code == 200