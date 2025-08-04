import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/item"

def test_create():
    payload = {
    "active": true,
    "cash_discount_group_id": 9624,
    "category_id": 8271,
    "description": "southern",
    "id": 804,
    "item_code": "affect",
    "name": "four",
    "price": 9025.1,
    "price_group_id": 5428,
    "secondary_category_id": 9820,
    "tax_group_id": 9812,
    "unit": "man",
    "upc_code": "long",
    "vendor_id": 4902
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/804")
    assert response.status_code == 200

def test_update():
    payload = {
    "active": true,
    "cash_discount_group_id": 9624,
    "category_id": 8271,
    "description": "southern",
    "id": 804,
    "item_code": "affect",
    "name": "four",
    "price": 9025.1,
    "price_group_id": 5428,
    "secondary_category_id": 9820,
    "tax_group_id": 9812,
    "unit": "man",
    "upc_code": "long",
    "vendor_id": 4902
}
    payload['id'] = 804
    response = httpx.put(f"{BASE_URL}/804", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/804")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?active=True")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?cash_discount_group_id=9624")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?category_id=8271")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?description=southern")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=804")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?item_code=affect")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=four")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?price=9025.1")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?price_group_id=5428")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?secondary_category_id=9820")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?tax_group_id=9812")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?unit=man")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?upc_code=long")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?vendor_id=4902")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?active__gt=0&active__lt=2")
    assert response.status_code == 200