import os
import json
import httpx
from datetime import datetime, timedelta

ENTITY = "inventory"
BASE = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
BASE_URL = f"{BASE}/api/{ENTITY}"
HAS_SINGLE_PK = True
PK_FIELDS = ["id"]
CREATED_ID = None

def _mk_parent(entity, body):
    url = f"{BASE}/api/{entity}"
    r = httpx.post(url, json=body)
    assert r.status_code in (200, 201), f"FK create failed: {entity} => {r.status_code} {r.text}"
    return r.json()

def _inject_fk(payload):
    p = dict(payload)
    parent = _mk_parent('item', json.loads('{"active": false, "cash_discount_group_id": 5248, "category_id": 4668, "description": "others", "id": 9732, "item_code": "move", "name": "hot", "price": 3215.77, "price_group_id": 3228, "secondary_category_id": 3545, "tax_group_id": 979, "unit": "interesting", "upc_code": "leave", "vendor_id": 8051}'))
    p['item_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('inventory_location', json.loads('{"address": "interesting", "id": 1361, "name": "improve"}'))
    p['location_id'] = parent.get('id', parent.get('id', 700001))
    return p

def _pk_filter_from_payload(p):
    params = {}
    for k in PK_FIELDS:
        if k in p:
            params[k] = p[k]
    return params

def test_create():
    global CREATED_ID
    payload = json.loads("{\"id\": 816, \"item_id\": 2934, \"location_id\": 9980, \"quantity\": 4845}")
    payload = _inject_fk(payload)
    response = httpx.post(BASE_URL, json=payload)
    assert response.status_code in (200, 201), response.text
    try:
        body = response.json() or {}
    except Exception:
        body = {}
    if isinstance(body, dict) and 'id' in body:
        CREATED_ID = body['id']
    elif isinstance(body, dict) and 'id' in body:
        CREATED_ID = body['id']
    elif isinstance(body, list) and body and isinstance(body[0], dict) and 'id' in body[0]:
        CREATED_ID = body[0]['id']
    else:
        CREATED_ID = 816
    assert isinstance(body, (dict, list))

def test_get_one():
    rid = CREATED_ID if 'CREATED_ID' in globals() and CREATED_ID else None
    rid = rid or 816
    resp = httpx.get(f"{BASE_URL}/{rid}")
    if resp.status_code == 404:
        payload = json.loads("{\"id\": 816, \"item_id\": 2934, \"location_id\": 9980, \"quantity\": 4845}")
        payload = _inject_fk(payload)
        payload['id'] = rid
        httpx.post(BASE_URL, json=payload)
        resp = httpx.get(f"{BASE_URL}/{rid}")
        if resp.status_code == 404:
            resp = httpx.get(BASE_URL, params={'id': rid})
    assert resp.status_code == 200, f"GET failed: {resp.status_code} {resp.text}"

def test_update():
    payload = json.loads("{\"id\": 816, \"item_id\": 2934, \"location_id\": 9980, \"quantity\": 4845}")
    payload = _inject_fk(payload)
    payload['id'] = 816
    httpx.post(BASE_URL, json=payload)
    response = httpx.put(f"{BASE_URL}/816", json=payload)
    assert response.status_code == 200

def test_delete():
    payload = json.loads("{\"id\": 816, \"item_id\": 2934, \"location_id\": 9980, \"quantity\": 4845}")
    payload = _inject_fk(payload)
    payload['id'] = 816
    httpx.post(BASE_URL, json=payload)
    response = httpx.delete(f"{BASE_URL}/816")
    assert response.status_code in (200, 204)

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_eq_id():
    response = httpx.get(BASE_URL, params={'id': 816})
    assert response.status_code == 200

def test_eq_item_id():
    response = httpx.get(BASE_URL, params={'item_id': 2934})
    assert response.status_code == 200

def test_eq_location_id():
    response = httpx.get(BASE_URL, params={'location_id': 9980})
    assert response.status_code == 200

def test_eq_quantity():
    response = httpx.get(BASE_URL, params={'quantity': 4845})
    assert response.status_code == 200

def test_date_filter():
    assert True  # no date-like field
