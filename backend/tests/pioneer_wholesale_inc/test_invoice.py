import os
import json
import httpx
from datetime import datetime, timedelta

ENTITY = "invoice"
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
    parent = _mk_parent('customer', json.loads('{"address": "marriage", "credit_limit": 3612.43, "email": "take", "id": 3333, "name": "start", "phone": "know", "salesperson_id": 8134}'))
    p['customer_id'] = parent.get('id', parent.get('id', 700001))
    return p

def _pk_filter_from_payload(p):
    params = {}
    for k in PK_FIELDS:
        if k in p:
            params[k] = p[k]
    return params

def test_create():
    global CREATED_ID
    payload = json.loads("{\"customer_id\": 7663, \"date\": \"2025-06-08T10:55:07.924611\", \"id\": 7380, \"status\": \"building\"}")
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
        CREATED_ID = 7380
    assert isinstance(body, (dict, list))

def test_get_one():
    rid = CREATED_ID if 'CREATED_ID' in globals() and CREATED_ID else None
    rid = rid or 7380
    resp = httpx.get(f"{BASE_URL}/{rid}")
    if resp.status_code == 404:
        payload = json.loads("{\"customer_id\": 7663, \"date\": \"2025-06-08T10:55:07.924611\", \"id\": 7380, \"status\": \"building\"}")
        payload = _inject_fk(payload)
        payload['id'] = rid
        httpx.post(BASE_URL, json=payload)
        resp = httpx.get(f"{BASE_URL}/{rid}")
        if resp.status_code == 404:
            resp = httpx.get(BASE_URL, params={'id': rid})
    assert resp.status_code == 200, f"GET failed: {resp.status_code} {resp.text}"

def test_update():
    payload = json.loads("{\"customer_id\": 7663, \"date\": \"2025-06-08T10:55:07.924611\", \"id\": 7380, \"status\": \"building\"}")
    payload = _inject_fk(payload)
    payload['id'] = 7380
    httpx.post(BASE_URL, json=payload)
    response = httpx.put(f"{BASE_URL}/7380", json=payload)
    assert response.status_code == 200

def test_delete():
    payload = json.loads("{\"customer_id\": 7663, \"date\": \"2025-06-08T10:55:07.924611\", \"id\": 7380, \"status\": \"building\"}")
    payload = _inject_fk(payload)
    payload['id'] = 7380
    httpx.post(BASE_URL, json=payload)
    response = httpx.delete(f"{BASE_URL}/7380")
    assert response.status_code in (200, 204)

def test_options():
    response = httpx.get(f"{BASE_URL}/options")
    assert response.status_code == 200

def test_eq_customer_id():
    response = httpx.get(BASE_URL, params={'customer_id': 7663})
    assert response.status_code == 200

def test_eq_id():
    response = httpx.get(BASE_URL, params={'id': 7380})
    assert response.status_code == 200

def test_eq_status():
    response = httpx.get(BASE_URL, params={'status': 'building'})
    assert response.status_code == 200

def test_date_filter():
    start = datetime.now() - timedelta(days=30)
    end = datetime.now() + timedelta(days=30)
    response = httpx.get(
        BASE_URL,
        params={'status__gt': start.isoformat(), 'status__lt': end.isoformat()}
)
    assert response.status_code == 200
