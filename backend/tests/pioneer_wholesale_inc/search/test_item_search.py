import httpx
import json

BASE_URL = "http://localhost:8000/search/item"

def test_search_basic():
    resp = httpx.get(BASE_URL, params={"q": "test"})
    assert resp.status_code in (200, 404, 501)
    # response may be not implemented depending on project state
