import os
import json
import httpx
from datetime import datetime, timedelta

ENTITY = "customer"
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
    parent = _mk_parent('salesperson', json.loads('{"email": "hair", "id": 2879, "name": "ahead", "phone": "trouble"}'))
    p['salesperson_id'] = parent.get('id', parent.get('id', 700001))
    return p

def _pk_filter_from_payload(p):
    params = {}
    for k in PK_FIELDS:
        if k in p:
            params[k] = p[k]
    return params

def test_create():
    global CREATED_ID
    payload = json.loads("{\"address\": \"customer\", \"credit_limit\": 9570.24, \"email\": \"commercial\", \"id\": 6623, \"name\": \"heart\", \"phone\": \"two\", \"salesperson_id\": 2105}")
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
        CREATED_ID = 6623
    assert isinstance(body, (dict, list))

def test_get_one():
    rid = CREATED_ID if 'CREATED_ID' in globals() and CREATED_ID else None
    rid = rid or 6623
    resp = httpx.get(f"{BASE_URL}/{rid}")
    if resp.status_code == 404:
        payload = json.loads("{\"address\": \"customer\", \"credit_limit\": 9570.24, \"email\": \"commercial\", \"id\": 6623, \"name\": \"heart\", \"phone\": \"two\", \"salesperson_id\": 2105}")
        payload = _inject_fk(payload)
        payload['id'] = rid
        httpx.post(BASE_URL, json=payload)
        resp = httpx.get(f"{BASE_URL}/{rid}")
        if resp.status_code == 404:
            resp = httpx.get(BASE_URL, params={'id': rid})
    assert resp.status_code == 200, f"GET failed: {resp.status_code} {resp.text}"

def test_update():
    payload = json.loads("{\"address\": \"customer\", \"credit_limit\": 9570.24, \"email\": \"commercial\", \"id\": 6623, \"name\": \"heart\", \"phone\": \"two\", \"salesperson_id\": 2105}")
    payload = _inject_fk(payload)
    payload['id'] = 6623
    httpx.post(BASE_URL, json=payload)
    response = httpx.put(f"{BASE_URL}/6623", json=payload)
    assert response.status_code == 200

def test_delete():
    payload = json.loads("{\"address\": \"customer\", \"credit_limit\": 9570.24, \"email\": \"commercial\", \"id\": 6623, \"name\": \"heart\", \"phone\": \"two\", \"salesperson_id\": 2105}")
    payload = _inject_fk(payload)
    payload['id'] = 6623
    httpx.post(BASE_URL, json=payload)
    response = httpx.delete(f"{BASE_URL}/6623")
    assert response.status_code in (200, 204)

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

# eq filters
def test_eq_address():
    response = httpx.get(BASE_URL, params={'address': 'customer'})
    assert response.status_code == 200

def test_eq_credit_limit():
    response = httpx.get(BASE_URL, params={'credit_limit': 9570.24})
    assert response.status_code == 200

def test_eq_email():
    response = httpx.get(BASE_URL, params={'email': 'commercial'})
    assert response.status_code == 200

def test_eq_id():
    response = httpx.get(BASE_URL, params={'id': 6623})
    assert response.status_code == 200

def test_eq_name():
    response = httpx.get(BASE_URL, params={'name': 'heart'})
    assert response.status_code == 200

def test_eq_phone():
    response = httpx.get(BASE_URL, params={'phone': 'two'})
    assert response.status_code == 200

def test_eq_salesperson_id():
    response = httpx.get(BASE_URL, params={'salesperson_id': 2105})
    assert response.status_code == 200

def test_date_filter():
    assert True  # no date-like field
