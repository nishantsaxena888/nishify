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
    parent = _mk_parent('purchase_order', json.loads('{"date": "2025-01-23T22:32:49.802311", "id": 649, "status": "there", "vendor_id": 1920}'))
    p['po_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('item', json.loads('{"active": false, "cash_discount_group_id": 6179, "category_id": 5828, "description": "write", "id": 5628, "item_code": "hit", "name": "action", "price": 1135.26, "price_group_id": 6155, "secondary_category_id": 5805, "tax_group_id": 9260, "unit": "authority", "upc_code": "structure", "vendor_id": 7926}'))
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
    payload = json.loads("{\"item_id\": 2694, \"po_id\": 7956, \"quantity\": 37, \"unit_price\": 8189.63}")
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
    payload = json.loads("{\"item_id\": 2694, \"po_id\": 7956, \"quantity\": 37, \"unit_price\": 8189.63}")
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
    response = httpx.get(BASE_URL, params={'item_id': 2694})
    assert response.status_code == 200

def test_eq_po_id():
    response = httpx.get(BASE_URL, params={'po_id': 7956})
    assert response.status_code == 200

def test_eq_quantity():
    response = httpx.get(BASE_URL, params={'quantity': 37})
    assert response.status_code == 200

def test_eq_unit_price():
    response = httpx.get(BASE_URL, params={'unit_price': 8189.63})
    assert response.status_code == 200

def test_date_filter():
    assert True  # no date-like field
