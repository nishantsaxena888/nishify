import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/secondary_category"

def test_create():
    payload = {
    "description": "surface",
    "id": 4249,
    "name": "support"
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/4249")
    assert response.status_code == 200

def test_update():
    payload = {
    "description": "surface",
    "id": 4249,
    "name": "support"
}
    payload['id'] = 4249
    response = httpx.put(f"{BASE_URL}/4249", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/4249")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?description=surface")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=4249")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=support")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=4248&id__lt=4250")
    assert response.status_code == 200