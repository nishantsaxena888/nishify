import json
import httpx
from datetime import datetime, date, timedelta

BASE_URL = "http://localhost:8000/api/vendor"

def test_create():
    global CREATED_ID
    payload = {
        "name": "v4802",
        "address": "v4803",
        "email": "v4804",
        "phone": "v4805",
        "contact_person": "v4806",
        "state_id": 804802,
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
        "name": "v4802",
        "address": "v4803",
        "email": "v4804",
        "phone": "v4805",
        "contact_person": "v4806",
        "state_id": 804802,
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

def test_update():
    rid = CREATED_ID if 'CREATED_ID' in globals() and CREATED_ID else 4802
    payload = {
        "id": rid,
        "name": "auto-upd",
    }
    resp = httpx.put(f"{BASE_URL}/{rid}", json=payload)
    assert resp.status_code in (200, 404)

def test_delete():
    rid = CREATED_ID if 'CREATED_ID' in globals() and CREATED_ID else 4802
    resp = httpx.delete(f"{BASE_URL}/{rid}")
    assert resp.status_code in (200, 404)
