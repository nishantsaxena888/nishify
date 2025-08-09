import os
import json
import httpx
from datetime import datetime, timedelta

ENTITY = "item"
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
    parent = _mk_parent('item_category', json.loads('{"description": "way", "id": 1168, "name": "thank"}'))
    p['category_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('secondary_category', json.loads('{"description": "range", "id": 2053, "name": "whatever"}'))
    p['secondary_category_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('vendor', json.loads('{"address": "attorney", "contact_person": "stay", "email": "plant", "id": 161, "name": "whose", "phone": "all", "state_id": 6691}'))
    p['vendor_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('tax_group', json.loads('{"id": 1481, "name": "they", "tax_percent": 3029.51}'))
    p['tax_group_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('price_group', json.loads('{"id": 4872, "markup_percent": 4095.71, "name": "owner"}'))
    p['price_group_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('cash_discount_group', json.loads('{"discount_percent": 4884.49, "id": 9152, "name": "sing", "terms": "out"}'))
    p['cash_discount_group_id'] = parent.get('id', parent.get('id', 700001))
    return p

def _pk_filter_from_payload(p):
    params = {}
    for k in PK_FIELDS:
        if k in p:
            params[k] = p[k]
    return params

def test_create():
    global CREATED_ID
    payload = json.loads("{\"active\": false, \"cash_discount_group_id\": 6179, \"category_id\": 5828, \"description\": \"write\", \"id\": 5628, \"item_code\": \"hit\", \"name\": \"action\", \"price\": 1135.26, \"price_group_id\": 6155, \"secondary_category_id\": 5805, \"tax_group_id\": 9260, \"unit\": \"authority\", \"upc_code\": \"structure\", \"vendor_id\": 7926}")
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
        CREATED_ID = 5628
    assert isinstance(body, (dict, list))

def test_get_one():
    rid = CREATED_ID if 'CREATED_ID' in globals() and CREATED_ID else None
    rid = rid or 5628
    resp = httpx.get(f"{BASE_URL}/{rid}")
    if resp.status_code == 404:
        payload = json.loads("{\"active\": false, \"cash_discount_group_id\": 6179, \"category_id\": 5828, \"description\": \"write\", \"id\": 5628, \"item_code\": \"hit\", \"name\": \"action\", \"price\": 1135.26, \"price_group_id\": 6155, \"secondary_category_id\": 5805, \"tax_group_id\": 9260, \"unit\": \"authority\", \"upc_code\": \"structure\", \"vendor_id\": 7926}")
        payload = _inject_fk(payload)
        payload['id'] = rid
        httpx.post(BASE_URL, json=payload)
        resp = httpx.get(f"{BASE_URL}/{rid}")
        if resp.status_code == 404:
            resp = httpx.get(BASE_URL, params={'id': rid})
    assert resp.status_code == 200, f"GET failed: {resp.status_code} {resp.text}"

def test_update():
    payload = json.loads("{\"active\": false, \"cash_discount_group_id\": 6179, \"category_id\": 5828, \"description\": \"write\", \"id\": 5628, \"item_code\": \"hit\", \"name\": \"action\", \"price\": 1135.26, \"price_group_id\": 6155, \"secondary_category_id\": 5805, \"tax_group_id\": 9260, \"unit\": \"authority\", \"upc_code\": \"structure\", \"vendor_id\": 7926}")
    payload = _inject_fk(payload)
    payload['id'] = 5628
    httpx.post(BASE_URL, json=payload)
    response = httpx.put(f"{BASE_URL}/5628", json=payload)
    assert response.status_code == 200

def test_delete():
    payload = json.loads("{\"active\": false, \"cash_discount_group_id\": 6179, \"category_id\": 5828, \"description\": \"write\", \"id\": 5628, \"item_code\": \"hit\", \"name\": \"action\", \"price\": 1135.26, \"price_group_id\": 6155, \"secondary_category_id\": 5805, \"tax_group_id\": 9260, \"unit\": \"authority\", \"upc_code\": \"structure\", \"vendor_id\": 7926}")
    payload = _inject_fk(payload)
    payload['id'] = 5628
    httpx.post(BASE_URL, json=payload)
    response = httpx.delete(f"{BASE_URL}/5628")
    assert response.status_code in (200, 204)

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_eq_active():
    response = httpx.get(BASE_URL, params={'active': False})
    assert response.status_code == 200

def test_eq_cash_discount_group_id():
    response = httpx.get(BASE_URL, params={'cash_discount_group_id': 6179})
    assert response.status_code == 200

def test_eq_category_id():
    response = httpx.get(BASE_URL, params={'category_id': 5828})
    assert response.status_code == 200

def test_eq_description():
    response = httpx.get(BASE_URL, params={'description': 'write'})
    assert response.status_code == 200

def test_eq_id():
    response = httpx.get(BASE_URL, params={'id': 5628})
    assert response.status_code == 200

def test_eq_item_code():
    response = httpx.get(BASE_URL, params={'item_code': 'hit'})
    assert response.status_code == 200

def test_eq_name():
    response = httpx.get(BASE_URL, params={'name': 'action'})
    assert response.status_code == 200

def test_eq_price():
    response = httpx.get(BASE_URL, params={'price': 1135.26})
    assert response.status_code == 200

def test_eq_price_group_id():
    response = httpx.get(BASE_URL, params={'price_group_id': 6155})
    assert response.status_code == 200

def test_eq_secondary_category_id():
    response = httpx.get(BASE_URL, params={'secondary_category_id': 5805})
    assert response.status_code == 200

def test_eq_tax_group_id():
    response = httpx.get(BASE_URL, params={'tax_group_id': 9260})
    assert response.status_code == 200

def test_eq_unit():
    response = httpx.get(BASE_URL, params={'unit': 'authority'})
    assert response.status_code == 200

def test_eq_upc_code():
    response = httpx.get(BASE_URL, params={'upc_code': 'structure'})
    assert response.status_code == 200

def test_eq_vendor_id():
    response = httpx.get(BASE_URL, params={'vendor_id': 7926})
    assert response.status_code == 200

def test_date_filter():
    assert True  # no date-like field
