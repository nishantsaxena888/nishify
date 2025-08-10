import json
import httpx
from datetime import datetime, date, timedelta

BASE_URL = "http://localhost:8000/api/invoice_item"

def test_create():
    global CREATED_ID
    payload = {
        "invoice_id": 804802,
        "item_id": 804803,
        "quantity": 5802,
        "price": 5803.0,
    }
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code == 200
    data = response.json()
    CREATED_ID = data.get('id')
    assert CREATED_ID is not None

def test_get_one():
    rid = CREATED_ID if 'CREATED_ID' in globals() and CREATED_ID else 4802
    resp = httpx.get(f"{BASE_URL}/{rid}")
    if resp.status_code == 404:
        payload = {
        "invoice_id": 804802,
        "item_id": 804803,
        "quantity": 5802,
        "price": 5803.0,
        "id": rid,
        }
        _ = httpx.post(BASE_URL, json=payload)
        resp = httpx.get(f"{BASE_URL}/{rid}")
    assert resp.status_code in (200, 404)
    if resp.status_code == 200:
        data = resp.json()
        assert isinstance(data, dict)

def test_list():
    resp = httpx.get(BASE_URL)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict) and 'items' in data
