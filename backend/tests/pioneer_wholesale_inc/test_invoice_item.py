import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/invoice_item"

def test_create():
    payload = {
    "invoice_id": 4559,
    "item_id": 7461,
    "price": 5173.48,
    "quantity": 5065
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/4559")
    assert response.status_code == 200

def test_update():
    payload = {
    "invoice_id": 4559,
    "item_id": 7461,
    "price": 5173.48,
    "quantity": 5065
}
    payload['invoice_id'] = 4559
    response = httpx.put(f"{BASE_URL}/4559", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/4559")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?invoice_id=4559")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?item_id=7461")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?price=5173.48")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?quantity=5065")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?invoice_id__gt=4558&invoice_id__lt=4560")
    assert response.status_code == 200