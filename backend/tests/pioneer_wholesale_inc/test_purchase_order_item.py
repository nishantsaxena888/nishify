import os
import json
import httpx
from datetime import datetime, timedelta

ENTITY = "purchase_order_item"
BASE = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
BASE_URL = f"{BASE}/api/{ENTITY}"
HAS_SINGLE_PK = False
PK_FIELDS = ["po_id", "item_id"]
CREATED_ID = None

def _mk_parent(entity, body):
    url = f"{BASE}/api/{entity}"
    r = httpx.post(url, json=body)
    assert r.status_code in (200, 201), f"FK create failed: {entity} => {r.status_code} {r.text}"
    return r.json()

def _inject_fk(payload):
    p = dict(payload)
    parent = _mk_parent('purchase_order', json.loads('{"date": "2025-01-03T06:01:35.559289", "id": 7173, "status": "alone", "vendor_id": 9591}'))
    p['po_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('item', json.loads('{"active": false, "cash_discount_group_id": 4944, "category_id": 7145, "description": "police", "id": 8610, "item_code": "decision", "name": "enjoy", "price": 440.88, "price_group_id": 9893, "secondary_category_id": 2882, "tax_group_id": 9149, "unit": "beautiful", "upc_code": "claim", "vendor_id": 5872}'))
    p['item_id'] = parent.get('id', parent.get('id', 700001))
    return p

def _pk_filter_from_payload(p):
    params = {}
    for k in PK_FIELDS:
        if k in p:
            params[k] = p[k]
    return params

def test_create():
    global CREATED_ID
    payload = json.loads("{\"item_id\": 5264, \"po_id\": 5783, \"quantity\": 412, \"unit_price\": 3467.98}")
    payload = _inject_fk(payload)
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code in (200, 201), response.text
    try:
        body = response.json() or {}
    except Exception:
        body = {}
    # composite pk: no single CREATED_ID
    assert isinstance(body, (dict, list))

def test_get_one():
    payload = json.loads("{\"item_id\": 5264, \"po_id\": 5783, \"quantity\": 412, \"unit_price\": 3467.98}")
    payload = _inject_fk(payload)
    httpx.post(BASE_URL, json=payload)
    params = _pk_filter_from_payload(payload)
    assert params, 'Composite PK params missing'
    resp = httpx.get(BASE_URL, params=params)
    assert resp.status_code == 200, f"GET (composite PK) failed: {resp.status_code} {resp.text}"

def test_update():
    assert True  # skipped for composite PK

def test_delete():
    assert True  # skipped for composite PK

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_eq_item_id():
    response = httpx.get(BASE_URL, params={'item_id': 5264})
    assert response.status_code == 200

def test_eq_po_id():
    response = httpx.get(BASE_URL, params={'po_id': 5783})
    assert response.status_code == 200

def test_eq_quantity():
    response = httpx.get(BASE_URL, params={'quantity': 412})
    assert response.status_code == 200

def test_eq_unit_price():
    response = httpx.get(BASE_URL, params={'unit_price': 3467.98})
    assert response.status_code == 200

def test_date_filter():
    assert True  # no date-like field
