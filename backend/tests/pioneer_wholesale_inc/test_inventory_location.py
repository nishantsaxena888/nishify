import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/inventory_location"

def test_create():
    payload = {
    "address": "list",
    "id": 8862,
    "name": "fly"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/8862")
    assert response.status_code == 200

def test_update():
    payload = {
    "address": "list",
    "id": 8862,
    "name": "fly"
}
    payload['id'] = 8862
    response = httpx.put(f"{BASE_URL}/8862", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/8862")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?address=list")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=8862")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=fly")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=8861&id__lt=8863")
    assert response.status_code == 200