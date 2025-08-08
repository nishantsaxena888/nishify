import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/invoice_item"

def test_create():
    payload = {
    "invoice_id": 2342,
    "item_id": 1937,
    "price": 8358.34,
    "quantity": 4153
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/2342")
    assert response.status_code == 200

def test_update():
    payload = {
    "invoice_id": 2342,
    "item_id": 1937,
    "price": 8358.34,
    "quantity": 4153
}
    payload['invoice_id'] = 2342
    response = httpx.put(f"{BASE_URL}/2342", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/2342")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?invoice_id=2342")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?item_id=1937")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?price=8358.34")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?quantity=4153")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?invoice_id__gt=2341&invoice_id__lt=2343")
    assert response.status_code == 200