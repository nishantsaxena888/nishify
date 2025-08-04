import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/purchase_order_item"

def test_create():
    payload = {
    "item_id": 7923,
    "po_id": 4870,
    "quantity": 9567,
    "unit_price": 5286.97
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/4870")
    assert response.status_code == 200

def test_update():
    payload = {
    "item_id": 7923,
    "po_id": 4870,
    "quantity": 9567,
    "unit_price": 5286.97
}
    payload['po_id'] = 4870
    response = httpx.put(f"{BASE_URL}/4870", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/4870")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?item_id=7923")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?po_id=4870")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?quantity=9567")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?unit_price=5286.97")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?item_id__gt=7922&item_id__lt=7924")
    assert response.status_code == 200