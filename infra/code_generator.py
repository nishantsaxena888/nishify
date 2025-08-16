#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client Code Generator (Jinja + fallbacks)
"""
import os, sys, csv, datetime, importlib, re
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, ChoiceLoader, DictLoader

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
from sqlalchemy.orm import relationship
from backend.utils.db import Base

def _sa_type(tname: str):
    t = (tname or "string").lower()
    if t in ("string", "str", "keyword", "varchar"): return String(255)
    if t in ("text",): return Text()
    if t in ("int", "integer"): return Integer()
    if t in ("float", "double", "number", "numeric"): return Float()
    if t in ("bool", "boolean"): return Boolean()
    if t in ("date",): return Date()
    if t in ("datetime", "timestamp"): return DateTime()
    return String(255)

{% set cls_name = entity|replace('-', ' ')|replace('_', ' ')|title|replace(' ', '') %}
class {{ cls_name }}(Base):
    __tablename__ = "{{ entity }}"

    {# ==== Columns ==== #}
    {% set fields = cfg.get("fields") or {} %}
    {% set has_pk = False %}
    {% for fname, spec in fields.items() %}
    {% set t = spec.get("type") %}
    {% set pk = spec.get("pk") or spec.get("primary_key") %}
    {% set fk0 = spec.get("fk") or spec.get("foreign_key") %}
    {% set uniq = spec.get("unique") %}
    {% set required = spec.get("required") %}
    {% set nullable = (False if required else (spec.get("nullable") if spec.get("nullable") is not none else None)) %}
    {% set fk = fk0 %}
    {% if not fk and fname.endswith('_id') and fname|length > 3 %}
        {% set fk = fname[:-3] + ".id" %}
    {% endif %}

    {% if pk %}
    {{ fname }} = Column(
        _sa_type("{{ t }}"),
        primary_key=True{% if (t or '')|lower in ['int','integer'] %}, autoincrement=True{% endif %}{% if uniq %}, unique=True{% endif %}{% if nullable is not none %}, nullable={{ 'True' if nullable else 'False' }}{% endif %}
    )
    {% set has_pk = True %}
    {% elif fk %}
    {% set parts = fk.split(".") %}
    {% set ref_table = parts[0] %}
    {% set ref_col = parts[1] if parts|length > 1 else "id" %}
    {{ fname }} = Column(
        _sa_type("{{ t }}"),
        ForeignKey("{{ ref_table }}.{{ ref_col }}"){% if uniq %}, unique=True{% endif %}{% if nullable is not none %}, nullable={{ 'True' if nullable else 'False' }}{% endif %}
    )
    {% else %}
    {{ fname }} = Column(
        _sa_type("{{ t }}"){% if uniq %}, unique=True{% endif %}{% if nullable is not none %}, nullable={{ 'True' if nullable else 'False' }}{% endif %}
    )
    {% endif %}

    {% endfor %}
    {% if not has_pk %}
    # Surrogate PK because schema had no pk
    id = Column(String(32), primary_key=True)
    {% endif %}

    {# ==== Unique Together ==== #}
    {% set ucs = cfg.get("unique_together") or [] %}
    {% if ucs %}
    __table_args__ = (
    {% for grp in ucs %}
        UniqueConstraint({% for c in grp %}"{{ c }}"{% if not loop.last %}, {% endif %}{% endfor %}, name="{{ entity }}_uniq_{{ loop.index0 }}"),
    {% endfor %}
    )
    {% endif %}

    {# ==== Child -> Parent relationships for FK fields ==== #}
    {% for fname, spec in fields.items() %}
    {% set fk = (spec.get("fk") or spec.get("foreign_key")) %}
    {% if not fk and fname.endswith('_id') and fname|length > 3 %}
        {% set fk = fname[:-3] + ".id" %}
    {% endif %}
    {% if fk %}
        {% set ref_table = fk.split(".")[0] %}
        {% set target_cls = ref_table|replace('-', ' ')|replace('_',' ')|title|replace(' ','') %}
        {% set rel_name = fname[:-3] if fname.endswith('_id') else fname + '_rel' %}
    {{ rel_name }} = relationship("{{ target_cls }}", foreign_keys=[{{ fname }}])
    {% endif %}
    {% endfor %}
"""

DEFAULT_HOOKS_J2 = r"""
# Auto-generated hooks for {{ client }}
from __future__ import annotations
from typing import Any, Dict, List
import datetime

# Static defaults only (simple literals). Dynamic timestamps handled below.
ENTITY_DEFAULTS: Dict[str, Dict[str, Any]] = {
{% for name, cfg in entities.items() %}
    "{{ name }}": {
    {%- for fname, fcfg in (cfg.get("fields") or {}).items() %}
        {%- if fcfg.get("default") is not none %}
        "{{ fname }}": {{ fcfg.get("default")|tojson }},
        {%- endif %}
    {%- endfor %}
    },
{% endfor %}
}

# Which entities have special timestamp behavior
ENTITY_TS_FLAGS: Dict[str, Dict[str, bool]] = {
{% for name, cfg in entities.items() %}
    "{{ name }}": {
        "has_created": {{ 'True' if 'created_at' in (cfg.get('fields') or {}) else 'False' }},
        "has_updated": {{ 'True' if 'updated_at' in (cfg.get('fields') or {}) else 'False' }},
    },
{% endfor %}
}

# auto_now fields per entity (set at request-time)
AUTO_NOW_FIELDS: Dict[str, List[str]] = {
{% for name, cfg in entities.items() %}
    "{{ name }}": [
    {%- for fname, fcfg in (cfg.get("fields") or {}).items() if (fcfg.get("type") in ("date","datetime","timestamp")) and fcfg.get("auto_now") %}
        "{{ fname }}",
    {%- endfor %}
    ],
{% endfor %}
}

def options(entity: str, schema: str = "basic") -> Dict[str, Any]:
    # Tests expect an OBJECT with 'entity' key
    return {"entity": entity, "schema": schema, "generated_for": "{{ client }}"}

def apply_defaults(entity: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.datetime.utcnow().isoformat() + "Z"
    defaults = ENTITY_DEFAULTS.get(entity) or {}
    out = dict(payload)

    # static defaults
    for k, v in defaults.items():
        out.setdefault(k, v)

    # dynamic auto_now fields
    for k in AUTO_NOW_FIELDS.get(entity, []):
        out.setdefault(k, now)

    # timestamps
    flags = ENTITY_TS_FLAGS.get(entity) or {}
    if flags.get("has_created"):
        out.setdefault("created_at", now)
    if flags.get("has_updated"):
        out["updated_at"] = now

    return out

def validate(entity: str, payload: Dict[str, Any]) -> List[str]:
    return []

def before_insert(entity: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return apply_defaults(entity, payload)

def after_insert(entity: str, record: Dict[str, Any]) -> Dict[str, Any]:
    return record

def before_update(entity: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(payload)
    if "updated_at" in ENTITY_TS_FLAGS.get(entity, {}):
        out = apply_defaults(entity, out)  # refresh updated_at
    return out

def after_update(entity: str, record: Dict[str, Any]) -> Dict[str, Any]:
    return record
"""

DEFAULT_TESTS_CRUD_J2 = r"""
# Auto-generated CRUD smoke tests for {{ client }}
from __future__ annotations import annotations
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
from __future__ annotations import annotations
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

def _class_name(name: str) -> str:
    return "".join(p.capitalize() for p in re.split(r'[_\W]+', name) if p)

def _infer_fk(field_name: str, spec: dict):
    fk = (spec or {}).get("fk") or (spec or {}).get("foreign_key")
    if fk:
        return fk.strip()
    if field_name.endswith("_id") and len(field_name) > 3:
        return f"{field_name[:-3]}.id"
    return None

def _incoming_fk_index(entities: Dict[str, Any]):
    """
    Build map: parent_entity -> list of child relationship descriptors.
    """
    incoming = {e: [] for e in entities.keys()}
    for child_entity, cfg in entities.items():
        fields = (cfg.get("fields") or {})
        for fname, spec in fields.items():
            fkspec = _infer_fk(fname, spec)
            if not fkspec:
                continue
            parent_table = fkspec.split(".")[0].strip()
            if parent_table not in incoming:
                continue
            rel_name = fname[:-3] if fname.endswith("_id") else f"{fname}_rel"
            incoming[parent_table].append({
                "child_entity": child_entity,
                "child_class": _class_name(child_entity),
                "child_field": fname,
                "child_rel_name": rel_name,
                "parent_collection": "items" if child_entity.endswith("_item") else f"{child_entity}s",
            })
    return incoming

def _fk_back_populates_for_entity(entity: str, entities: Dict[str, Any]):
    """
    For each FK field on this entity, compute collection name on parent.
    """
    back = {}
    for fname, spec in (entities[entity].get("fields") or {}).items():
        if _infer_fk(fname, spec):
            back[fname] = "items" if entity.endswith("_item") else f"{entity}s"
    return back

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

    incoming = _incoming_fk_index(entities)

    for name, cfg in entities.items():
        fields = cfg.get("fields") or {}
        has_pk = any((isinstance(v, dict) and v.get("pk")) for v in fields.values())
        safe_cfg = cfg if has_pk else {**cfg, "fields": {"id": {"type": "string", "pk": True}, **fields}}

        rendered = tpl.render(
            client=client,
            entity=name,
            cfg=safe_cfg,
            entities=entities,
            now=_now_iso(),
            incoming_children=incoming.get(name, []),
            fk_back_populates=_fk_back_populates_for_entity(name, entities),
        )
        out_path = os.path.join(pkg_dir, f"{name}.py")
        _write_text(out_path, rendered)
        print(f"[codegen] wrote {out_path}")

    # ensure string relationships resolve by importing all classes
    init_lines = [f"from .{n} import {_class_name(n)}" for n in entities.keys()]
    _write_text(os.path.join(pkg_dir, "__init__.py"), "\n".join(init_lines) + "\n")
    print(f"[codegen] wrote {os.path.join(pkg_dir, '__init__.py')}")

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
    _ensure_pkg(out_dir)
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
