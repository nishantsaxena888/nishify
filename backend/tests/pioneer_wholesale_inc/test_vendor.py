import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/vendor"

def test_create():
    payload = {
    "address": "art",
    "contact_person": "everyone",
    "email": "write",
    "id": 545,
    "name": "result",
    "phone": "defense",
    "state_id": 4978
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/545")
    assert response.status_code == 200

def test_update():
    payload = {
    "address": "art",
    "contact_person": "everyone",
    "email": "write",
    "id": 545,
    "name": "result",
    "phone": "defense",
    "state_id": 4978
}
    payload['id'] = 545
    response = httpx.put(f"{BASE_URL}/545", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/545")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?address=art")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?contact_person=everyone")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?email=write")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=545")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=result")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?phone=defense")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?state_id=4978")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?id__gt=544&id__lt=546")
    assert response.status_code == 200