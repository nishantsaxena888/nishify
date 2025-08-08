import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/item"

def test_create():
    payload = {
    "active": true,
    "cash_discount_group_id": 6435,
    "category_id": 6452,
    "description": "seat",
    "id": 5392,
    "item_code": "whether",
    "name": "collection",
    "price": 2483.47,
    "price_group_id": 6737,
    "secondary_category_id": 6208,
    "tax_group_id": 6437,
    "unit": "worry",
    "upc_code": "necessary",
    "vendor_id": 6378
}
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    assert response.json().get('success')

def test_get_one():
    response = httpx.get(f"{BASE_URL}/5392")
    assert response.status_code == 200

def test_update():
    payload = {
    "active": true,
    "cash_discount_group_id": 6435,
    "category_id": 6452,
    "description": "seat",
    "id": 5392,
    "item_code": "whether",
    "name": "collection",
    "price": 2483.47,
    "price_group_id": 6737,
    "secondary_category_id": 6208,
    "tax_group_id": 6437,
    "unit": "worry",
    "upc_code": "necessary",
    "vendor_id": 6378
}
    payload['id'] = 5392
    response = httpx.put(f"{BASE_URL}/5392", json=payload)
    assert response.status_code == 200

def test_delete():
    response = httpx.delete(f"{BASE_URL}/5392")
    assert response.status_code == 200

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_list_eq():
    response = httpx.get(f"{BASE_URL}?active=True")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?cash_discount_group_id=6435")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?category_id=6452")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?description=seat")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?id=5392")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?item_code=whether")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?name=collection")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?price=2483.47")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?price_group_id=6737")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?secondary_category_id=6208")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?tax_group_id=6437")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?unit=worry")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?upc_code=necessary")
    assert response.status_code == 200
    response = httpx.get(f"{BASE_URL}?vendor_id=6378")
    assert response.status_code == 200

def test_range_gt_lt():
    response = httpx.get(f"{BASE_URL}?active__gt=0&active__lt=2")
    assert response.status_code == 200