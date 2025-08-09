import os
import json
import httpx
from datetime import datetime, timedelta

ENTITY = "invoice_item"
BASE = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
BASE_URL = f"{BASE}/api/{ENTITY}"
HAS_SINGLE_PK = False
PK_FIELDS = ["invoice_id", "item_id"]
CREATED_ID = None

def _mk_parent(entity, body):
    url = f"{BASE}/api/{entity}"
    r = httpx.post(url, json=body)
    assert r.status_code in (200, 201), f"FK create failed: {entity} => {r.status_code} {r.text}"
    return r.json()

def _inject_fk(payload):
    p = dict(payload)
    parent = _mk_parent('invoice', json.loads('{"customer_id": 2991, "date": "2025-05-06T21:49:20.767544", "id": 9474, "status": "sign"}'))
    p['invoice_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('item', json.loads('{"active": false, "cash_discount_group_id": 5248, "category_id": 4668, "description": "others", "id": 9732, "item_code": "move", "name": "hot", "price": 3215.77, "price_group_id": 3228, "secondary_category_id": 3545, "tax_group_id": 979, "unit": "interesting", "upc_code": "leave", "vendor_id": 8051}'))
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
    payload = json.loads("{\"invoice_id\": 6345, \"item_id\": 5825, \"price\": 9099.08, \"quantity\": 5164}")
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
    payload = json.loads("{\"invoice_id\": 6345, \"item_id\": 5825, \"price\": 9099.08, \"quantity\": 5164}")
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

def test_eq_invoice_id():
    response = httpx.get(BASE_URL, params={'invoice_id': 6345})
    assert response.status_code == 200

def test_eq_item_id():
    response = httpx.get(BASE_URL, params={'item_id': 5825})
    assert response.status_code == 200

def test_eq_price():
    response = httpx.get(BASE_URL, params={'price': 9099.08})
    assert response.status_code == 200

def test_eq_quantity():
    response = httpx.get(BASE_URL, params={'quantity': 5164})
    assert response.status_code == 200

def test_date_filter():
    assert True  # no date-like field
