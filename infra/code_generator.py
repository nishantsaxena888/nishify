#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client Code Generator (Jinja + fallbacks)
"""
import os, sys, csv, datetime, importlib
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, ChoiceLoader, DictLoader, TemplateNotFound

# ----------------- DEFAULT TEMPLATES (fallbacks) -----------------

DEFAULT_MODEL_J2 = r"""
# AUTO-GENERATED: {{ entity }} model for {{ client }} ({{ now }})
# Source: clients/{{ client }}/entities.py
# Do NOT edit manually.

from __future__ import annotations
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Date, DateTime,
    ForeignKey, UniqueConstraint, Text
)
from backend.utils.db import Base

def _sa_type(tname: str):
    t = (tname or "string").lower()
    if t in ("string", "keyword", "varchar"): return String(255)
    if t in ("text",): return Text()
    if t in ("int", "integer"): return Integer()
    if t in ("float", "double", "number", "numeric"): return Float()
    if t in ("bool", "boolean"): return Boolean()
    if t in ("date",): return Date()
    if t in ("datetime", "timestamp"): return DateTime()
    return String(255)

class {{ entity|replace('-', ' ')|replace('_', ' ')|title|replace(' ', '') }}(Base):
    __tablename__ = "{{ entity }}"

    {% set fields = cfg.get("fields") or {} %}
    {% set has_pk = False %}
    {% for fname, spec in fields.items() %}
    {% set t = spec.get("type") %}
    {% set pk = spec.get("pk") %}
    {% set fk = spec.get("fk") %}
    {% set uniq = spec.get("unique") %}
    {% set required = spec.get("required") %}
    {% set nullable =
         (False if required else
          (spec.get("nullable") if spec.get("nullable") is not none else None)) %}

    {% if pk %}
    {{ fname }} = Column(_sa_type("{{ t }}"), primary_key=True{% if uniq %}, unique=True{% endif %}{% if nullable is not none %}, nullable={{ nullable|lower }}{% endif %})
    {% set has_pk = True %}
    {% elif fk %}
    {% set parts = fk.split(".") %}
    {% set ref_table = parts[0] %}
    {% set ref_col = parts[1] if parts|length > 1 else "id" %}
    {{ fname }} = Column(_sa_type("{{ t }}"), ForeignKey("{{ ref_table }}.{{ ref_col }}"){% if uniq %}, unique=True{% endif %}{% if nullable is not none %}, nullable={{ nullable|lower }}{% endif %})
    {% else %}
    {{ fname }} = Column(_sa_type("{{ t }}"){% if uniq %}, unique=True{% endif %}{% if nullable is not none %}, nullable={{ nullable|lower }}{% endif %})
    {% endif %}

    {% endfor %}
    {% if not has_pk %}
    id = Column(String(32), primary_key=True)
    {% endif %}

    {% set ucs = cfg.get("unique_together") or [] %}
    {% if ucs %}
    __table_args__ = (
    {% for grp in ucs %}
        UniqueConstraint({% for c in grp %}"{{ c }}"{% if not loop.last %}, {% endif %}{% endfor %}, name="{{ entity }}_uniq_{{ loop.index0 }}"),
    {% endfor %}
    )
    {% endif %}
"""

DEFAULT_HOOKS_J2 = r"""
# Auto-generated hooks for {{ client }}
from __future__ import annotations
from typing import Any, Dict, List
import datetime

ENTITY_DEFAULTS: Dict[str, Dict[str, Any]] = {
{% for name, cfg in entities.items() %}
    "{{ name }}": {
    {%- for fname, fcfg in (cfg.get("fields") or {}).items() %}
        {%- if fcfg.get("default") is not none %}
        "{{ fname }}": {{ fcfg.get("default")|tojson }},
        {%- elif (fcfg.get("type") in ("date","datetime","timestamp")) and fcfg.get("auto_now") %}
        "{{ fname }}": datetime.datetime.utcnow().isoformat() + "Z",
        {%- endif %}
    {%- endfor %}
    },
{% endfor %}
}

def options(entity: str, schema: str = "basic") -> Dict[str, Any]:
    return {"entity": entity, "schema": schema, "generated_for": "{{ client }}"}

def apply_defaults(entity: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    defaults = ENTITY_DEFAULTS.get(entity) or {}
    out = dict(payload)
    for k, v in defaults.items():
        out.setdefault(k, v)
    if "created_at" in out and not out.get("created_at"):
        out["created_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    if "updated_at" in out:
        out["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    return out

def validate(entity: str, payload: Dict[str, Any]) -> List[str]:
    return []

def before_insert(entity: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return apply_defaults(entity, payload)

def after_insert(entity: str, record: Dict[str, Any]) -> Dict[str, Any]:
    return record

def before_update(entity: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(payload)
    if "updated_at" in out:
        out["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    return out

def after_update(entity: str, record: Dict[str, Any]) -> Dict[str, Any]:
    return record
"""

DEFAULT_TESTS_CRUD_J2 = r"""
# Auto-generated CRUD smoke tests for {{ client }}
from __future__ import annotations
import pytest
from fastapi.testclient import TestClient

try:
    from backend.main import app
except Exception as e:
    raise RuntimeError("Could not import backend.main:app for tests") from e

from clients.{{ client }}.entities_data import sample_data as _SAMPLE

client = TestClient(app)

ENTITIES = [
{% for name, cfg in entities.items() %}
    "{{ name }}",
{% endfor %}
]

@pytest.mark.parametrize("entity", ENTITIES)
def test_options_basic_and_full(entity):
    r1 = client.get(f"/api/{entity}/options")
    assert r1.status_code == 200, r1.text
    assert r1.json().get("entity") == entity

    r2 = client.get(f"/api/{entity}/options?schema=full")
    assert r2.status_code == 200, r2.text
    assert r2.json().get("entity") == entity

@pytest.mark.parametrize("entity", ENTITIES)
def test_list_minimal(entity):
    r = client.get(f"/api/{entity}", params={"skip": 0, "limit": 5})
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data, dict), "List response should be an object"
    assert isinstance(data.get("items"), list), "items must be a list"
"""

DEFAULT_TESTS_FILTERS_J2 = r"""
# Auto-generated filter/search tests for {{ client }}
from __future__ import annotations
import pytest
from fastapi.testclient import TestClient

try:
    from backend.main import app
except Exception as e:
    raise RuntimeError("Could not import backend.main:app for tests") from e

from clients.{{ client }}.entities_data import sample_data as _SAMPLE

client = TestClient(app)

ENTITIES = [
{% for name, cfg in entities.items() %}
    "{{ name }}",
{% endfor %}
]

@pytest.mark.parametrize("entity", ENTITIES)
def test_filter_eq(entity):
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
    assert any(str(v.get(field)) == str(value) for v in items)

@pytest.mark.parametrize("entity", ENTITIES)
def test_filter_gt_lt(entity):
    rows = _SAMPLE.get(entity) or []
    if not rows:
        pytest.skip(f"no sample rows for {entity}")
    num_field = None
    for k, v in rows[0].items():
        if isinstance(v, (int, float)):
            num_field = k
            break
    if not num_field:
        pytest.skip(f"no numeric fields in {entity}")
    val = rows[0][num_field]
    r1 = client.get(f"/api/{entity}", params={f"{num_field}__gt": val})
    assert r1.status_code == 200, r1.text
    r2 = client.get(f"/api/{entity}", params={f"{num_field}__lt": val})
    assert r2.status_code == 200, r2.text
"""

# ----------------- Jinja env -----------------

def get_jinja_env() -> Environment:
    return Environment(
        loader=ChoiceLoader([
            FileSystemLoader("infra/templates"),
            DictLoader({
                "backend/model.py.j2": DEFAULT_MODEL_J2,
                "backend/hooks.py.j2": DEFAULT_HOOKS_J2,
                "backend/tests_crud.py.j2": DEFAULT_TESTS_CRUD_J2,
                "backend/tests_filters.py.j2": DEFAULT_TESTS_FILTERS_J2,
            }),
        ]),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )

# ----------------- utils -----------------

def _import(path: str):
    return importlib.import_module(path)

def _write_text(path: str, text: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def _now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def _normalize_fields(cfg: dict) -> dict:
    fields = {}
    for fname, spec in (cfg.get("fields") or {}).items():
        s = dict(spec)
        if s.get("primary_key") and not s.get("pk"):
            s["pk"] = True
        if s.get("foreign_key") and not s.get("fk"):
            s["fk"] = s["foreign_key"]
        fields[fname] = s
    return {**cfg, "fields": fields}

def _ensure_pkg(path_dir: str):
    """Make every segment a package by adding __init__.py."""
    here = ""
    for part in path_dir.split(os.sep):
        here = part if here == "" else os.path.join(here, part)
        if not os.path.isdir(here):
            os.makedirs(here, exist_ok=True)
        initp = os.path.join(here, "__init__.py")
        if not os.path.exists(initp):
            open(initp, "a").close()

def load_entities(client: str) -> Dict[str, Any]:
    mod = _import(f"clients.{client}.entities")
    entities = getattr(mod, "entities", None)
    if not isinstance(entities, dict):
        raise SystemExit(f"ERROR: clients/{client}/entities.py must define `entities` dict")
    return {name: _normalize_fields(cfg) for name, cfg in entities.items()}

def load_sample_data(client: str) -> Dict[str, Any]:
    try:
        m = _import(f"clients.{client}.entities_data")
        return getattr(m, "sample_data")
    except Exception as e:
        raise SystemExit(
            f"ERROR: Could not import clients.{client}.entities_data.sample_data.\n"
            f"Run: CLIENT_NAME={client} python -m infra.data_faker"
        ) from e

def _assert_pks(entities: Dict[str, Any]):
    missing = [
        n for n, c in entities.items()
        if not any((isinstance(v, dict) and v.get("pk")) for v in (c.get("fields") or {}).values())
    ]
    if missing:
        print(f"[codegen] NOTE: Injecting surrogate PK 'id' for: {', '.join(missing)}")

# ----------------- generators -----------------

def generate_models(env: Environment, client: str, entities: Dict[str, Any]):
    tpl = env.get_template("backend/model.py.j2")
    _assert_pks(entities)
    pkg_dir = os.path.join("backend", "clients", client, "models")
    _ensure_pkg(os.path.join("backend"))
    _ensure_pkg(os.path.join("backend", "clients"))
    _ensure_pkg(os.path.join("backend", "clients", client))
    _ensure_pkg(pkg_dir)
    for name, cfg in entities.items():
        fields = cfg.get("fields") or {}
        has_pk = any((isinstance(v, dict) and v.get("pk")) for v in fields.values())
        safe_cfg = cfg if has_pk else {**cfg, "fields": {"id": {"type": "string", "pk": True}, **fields}}
        out_path = os.path.join(pkg_dir, f"{name}.py")
        rendered = tpl.render(client=client, entity=name, cfg=safe_cfg, entities=entities, now=_now_iso())
        _write_text(out_path, rendered)
        print(f"[codegen] wrote {out_path}")

def generate_hooks(env: Environment, client: str, entities: Dict[str, Any]):
    tpl = env.get_template("backend/hooks.py.j2")
    out_path = os.path.join("backend", "clients", client, "hooks.py")
    _ensure_pkg(os.path.join("backend", "clients", client))
    rendered = tpl.render(client=client, entities=entities, now=_now_iso())
    _write_text(out_path, rendered)
    print(f"[codegen] wrote {out_path}")

def generate_tests(env: Environment, client: str, entities: Dict[str, Any]):
    tpl_crud = env.get_template("backend/tests_crud.py.j2")
    tpl_filters = env.get_template("backend/tests_filters.py.j2")
    out_dir = os.path.join("backend", "clients", client, "tests")
    _ensure_pkg(os.path.join("backend", "clients", client, "tests"))
    _write_text(os.path.join(out_dir, "test_crud.py"), tpl_crud.render(client=client, entities=entities, now=_now_iso()))
    _write_text(os.path.join(out_dir, "test_filters.py"), tpl_filters.render(client=client, entities=entities, now=_now_iso()))
    print(f"[codegen] wrote {os.path.join(out_dir, 'test_crud.py')}")
    print(f"[codegen] wrote {os.path.join(out_dir, 'test_filters.py')}")

def generate_excel_samples(client: str, entities: Dict[str, Any], sample_data: Dict[str, Any]):
    base_dir = os.path.join("backend", "clients", client, "excel")
    os.makedirs(base_dir, exist_ok=True)
    for name, cfg in entities.items():
        fields = list((cfg.get("fields") or {}).keys())
        if not fields:
            continue
        sample_rows = sample_data.get(name) or []
        out_path = os.path.join(base_dir, f"{name}_sample.csv")
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            if sample_rows:
                for row in sample_rows[:3]:
                    writer.writerow({k: row.get(k, "") for k in fields})
            else:
                writer.writerow({k: "" for k in fields})
        print(f"[codegen] wrote {out_path}")

# ----------------- main -----------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m infra.code_generator <client_name>")
        raise SystemExit(2)
    client = sys.argv[1].strip()
    env = get_jinja_env()
    entities = load_entities(client)
    sample_data = load_sample_data(client)
    generate_models(env, client, entities)
    generate_hooks(env, client, entities)
    generate_excel_samples(client, entities, sample_data)
    generate_tests(env, client, entities)
    print("[codegen] All done.")

if __name__ == "__main__":
    main()
