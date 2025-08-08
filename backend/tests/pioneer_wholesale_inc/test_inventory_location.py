import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/inventory_location"

def test_create():
    payload = {
    "address": "use",
    "id": 3098,
    "name": "material"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/3098")
    assert response.status_code == 200

def test_update():
    payload = {
    "address": "use",
    "id": 3098,
    "name": "material"
}
    payload['id'] = 3098
    response = httpx.put(f"{BASE_URL}/3098", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/3098")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?address=use")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=3098")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=material")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=3097&id__lt=3099")
    assert response.status_code == 200