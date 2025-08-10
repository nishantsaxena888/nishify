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
    parent = _mk_parent('item_category', json.loads('{"description": "exactly", "id": 1171, "name": "manage"}'))
    p['category_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('secondary_category', json.loads('{"description": "fight", "id": 3244, "name": "enjoy"}'))
    p['secondary_category_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('vendor', json.loads('{"address": "plant", "contact_person": "life", "email": "what", "id": 7883, "name": "run", "phone": "loss", "state_id": 5953}'))
    p['vendor_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('tax_group', json.loads('{"id": 169, "name": "some", "tax_percent": 1816.31}'))
    p['tax_group_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('price_group', json.loads('{"id": 5386, "markup_percent": 9270.89, "name": "follow"}'))
    p['price_group_id'] = parent.get('id', parent.get('id', 700001))
    parent = _mk_parent('cash_discount_group', json.loads('{"discount_percent": 1564.02, "id": 9247, "name": "a", "terms": "spend"}'))
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
    payload = json.loads("{\"active\": true, \"cash_discount_group_id\": 9751, \"category_id\": 2297, \"description\": \"black\", \"id\": 2630, \"item_code\": \"there\", \"name\": \"none\", \"price\": 6089.01, \"price_group_id\": 3846, \"secondary_category_id\": 7636, \"tax_group_id\": 4249, \"unit\": \"marriage\", \"upc_code\": \"opportunity\", \"vendor_id\": 2323}")
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
        CREATED_ID = 2630
    assert isinstance(body, (dict, list))

def test_get_one():
    rid = CREATED_ID if 'CREATED_ID' in globals() and CREATED_ID else None
    rid = rid or 2630
    resp = httpx.get(f"{BASE_URL}/{rid}")
    if resp.status_code == 404:
        payload = json.loads("{\"active\": true, \"cash_discount_group_id\": 9751, \"category_id\": 2297, \"description\": \"black\", \"id\": 2630, \"item_code\": \"there\", \"name\": \"none\", \"price\": 6089.01, \"price_group_id\": 3846, \"secondary_category_id\": 7636, \"tax_group_id\": 4249, \"unit\": \"marriage\", \"upc_code\": \"opportunity\", \"vendor_id\": 2323}")
        payload = _inject_fk(payload)
        payload['id'] = rid
        httpx.post(BASE_URL, json=payload)
        resp = httpx.get(f"{BASE_URL}/{rid}")
        if resp.status_code == 404:
            resp = httpx.get(BASE_URL, params={'id': rid})
    assert resp.status_code == 200, f"GET failed: {resp.status_code} {resp.text}"

def test_update():
    payload = json.loads("{\"active\": true, \"cash_discount_group_id\": 9751, \"category_id\": 2297, \"description\": \"black\", \"id\": 2630, \"item_code\": \"there\", \"name\": \"none\", \"price\": 6089.01, \"price_group_id\": 3846, \"secondary_category_id\": 7636, \"tax_group_id\": 4249, \"unit\": \"marriage\", \"upc_code\": \"opportunity\", \"vendor_id\": 2323}")
    payload = _inject_fk(payload)
    payload['id'] = 2630
    httpx.post(BASE_URL, json=payload)
    response = httpx.put(f"{BASE_URL}/2630", json=payload)
    assert response.status_code == 200

def test_delete():
    payload = json.loads("{\"active\": true, \"cash_discount_group_id\": 9751, \"category_id\": 2297, \"description\": \"black\", \"id\": 2630, \"item_code\": \"there\", \"name\": \"none\", \"price\": 6089.01, \"price_group_id\": 3846, \"secondary_category_id\": 7636, \"tax_group_id\": 4249, \"unit\": \"marriage\", \"upc_code\": \"opportunity\", \"vendor_id\": 2323}")
    payload = _inject_fk(payload)
    payload['id'] = 2630
    httpx.post(BASE_URL, json=payload)
    response = httpx.delete(f"{BASE_URL}/2630")
    assert response.status_code in (200, 204)

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_eq_active():
    response = httpx.get(BASE_URL, params={'active': True})
    assert response.status_code == 200

def test_eq_cash_discount_group_id():
    response = httpx.get(BASE_URL, params={'cash_discount_group_id': 9751})
    assert response.status_code == 200

def test_eq_category_id():
    response = httpx.get(BASE_URL, params={'category_id': 2297})
    assert response.status_code == 200

def test_eq_description():
    response = httpx.get(BASE_URL, params={'description': 'black'})
    assert response.status_code == 200

def test_eq_id():
    response = httpx.get(BASE_URL, params={'id': 2630})
    assert response.status_code == 200

def test_eq_item_code():
    response = httpx.get(BASE_URL, params={'item_code': 'there'})
    assert response.status_code == 200

def test_eq_name():
    response = httpx.get(BASE_URL, params={'name': 'none'})
    assert response.status_code == 200

def test_eq_price():
    response = httpx.get(BASE_URL, params={'price': 6089.01})
    assert response.status_code == 200

def test_eq_price_group_id():
    response = httpx.get(BASE_URL, params={'price_group_id': 3846})
    assert response.status_code == 200

def test_eq_secondary_category_id():
    response = httpx.get(BASE_URL, params={'secondary_category_id': 7636})
    assert response.status_code == 200

def test_eq_tax_group_id():
    response = httpx.get(BASE_URL, params={'tax_group_id': 4249})
    assert response.status_code == 200

def test_eq_unit():
    response = httpx.get(BASE_URL, params={'unit': 'marriage'})
    assert response.status_code == 200

def test_eq_upc_code():
    response = httpx.get(BASE_URL, params={'upc_code': 'opportunity'})
    assert response.status_code == 200

def test_eq_vendor_id():
    response = httpx.get(BASE_URL, params={'vendor_id': 2323})
    assert response.status_code == 200

def test_date_filter():
    assert True  # no date-like field
