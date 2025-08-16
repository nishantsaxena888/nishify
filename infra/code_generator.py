#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client Code Generator (loads Jinja templates from infra/templates)
"""
import os
import sys
import csv
import datetime
import importlib
import re
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader

# ----------------- Jinja env -----------------

def get_jinja_env() -> Environment:
    return Environment(
        loader=FileSystemLoader("infra/templates"),
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
    tpl = env.get_template("backend/models.py.j2")
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
    out_dir = os.path.join("backend", "tests", client)
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
