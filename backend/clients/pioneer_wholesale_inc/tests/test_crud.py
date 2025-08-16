# Auto-generated CRUD smoke tests for pioneer_wholesale_inc
from __future__ import annotations
import pytest
from fastapi.testclient import TestClient

try:
    # Your FastAPI entrypoint should expose `app`
    from backend.main import app
except Exception as e:  # pragma: no cover
    raise RuntimeError("Could not import backend.main:app for tests") from e

# Import generated sample data (used only to ensure entities exist)
from clients.pioneer_wholesale_inc.entities_data import sample_data as _SAMPLE

client = TestClient(app)

# Entities under test (in generator-provided order)
ENTITIES = [    "state",    "item_category",    "secondary_category",    "vendor",    "item",    "tax_group",    "cash_discount_group",    "price_group",    "inventory_location",    "inventory",    "salesperson",    "customer",    "purchase_order",    "purchase_order_item",    "invoice",    "invoice_item",]

@pytest.mark.parametrize("entity", ENTITIES)
def test_options_basic_and_full(entity):
    r1 = client.get(f"/api/{entity}/options")
    assert r1.status_code == 200, r1.text
    j1 = r1.json()
    assert j1.get("entity") == entity

    r2 = client.get(f"/api/{entity}/options?schema=full")
    assert r2.status_code == 200, r2.text
    j2 = r2.json()
    assert j2.get("entity") == entity

@pytest.mark.parametrize("entity", ENTITIES)
def test_list_minimal(entity):
    # Simple list with pagination params should not error
    r = client.get(f"/api/{entity}", params={"skip": 0, "limit": 5})
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data, dict), "List response should be an object with 'items' or similar"
    # Allow both shapes: either {"items": [...]} or plain list for legacy
    items = data.get("items") if isinstance(data, dict) else data
    assert items is not None, "Response missing 'items' field"
    assert isinstance(items, list), "items should be a list"