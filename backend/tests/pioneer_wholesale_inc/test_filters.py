# Auto-generated filter/search tests for pioneer_wholesale_inc
from __future__ import annotations
import pytest
from fastapi.testclient import TestClient

try:
    from backend.main import app
except Exception as e:  # pragma: no cover
    raise RuntimeError("Could not import backend.main:app for tests") from e

from clients.pioneer_wholesale_inc.entities_data import sample_data as _SAMPLE

client = TestClient(app)

ENTITIES = [    "state",    "item_category",    "secondary_category",    "vendor",    "item",    "tax_group",    "cash_discount_group",    "price_group",    "inventory_location",    "inventory",    "salesperson",    "customer",    "purchase_order",    "purchase_order_item",    "invoice",    "invoice_item",]

@pytest.mark.parametrize("entity", ENTITIES)
def test_filter_eq(entity):
    # Pick one field from sample data to filter on
    rows = _SAMPLE.get(entity) or []
    if not rows:
        pytest.skip(f"no sample rows for {entity}")
    row = rows[0]
    field, value = next(iter(row.items()))
    r = client.get(f"/api/{entity}", params={field: value})
    assert r.status_code == 200, r.text
    data = r.json()
    items = data.get("items") if isinstance(data, dict) else data
    assert isinstance(items, list)
    assert isinstance(data, dict)
    assert data['items'] == items
    assert data['page'] == 1
    assert data['size'] == 20
    assert isinstance(data['total'], int) and data['total'] >= 0


@pytest.mark.parametrize("entity", ENTITIES)
def test_filter_gt_lt(entity):
    rows = _SAMPLE.get(entity) or []
    if not rows:
        pytest.skip(f"no sample rows for {entity}")
    # choose first numeric field if any
    num_field = None
    for k,v in rows[0].items():
        if isinstance(v, (int,float)):
            num_field = k
            break
    if not num_field:
        pytest.skip(f"no numeric fields in {entity}")
    val = rows[0][num_field]
    # test gt
    r1 = client.get(f"/api/{entity}", params={f"{num_field}__gt": val})
    assert r1.status_code == 200
    # test lt
    r2 = client.get(f"/api/{entity}", params={f"{num_field}__lt": val})
    assert r2.status_code == 200