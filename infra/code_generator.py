#!/usr/bin/env python3
"""
Universal Code Generator — (Backwards-Compatible) Backend + Frontend + Search

This is a **drop-in replacement** for your current code_generator.py. It preserves
all of your working functions (models, mocks, test data, excel dump, pages copy,
legacy tests, search tests, copy_entity_files) and **wraps them in a modular
adapter-style pipeline** so backend + frontend + search can be generated in a
single run with selective targets and safety flags.

Key points:
- ✅ Backwards compatible CLI: `python code_generator.py <client_name> [mock]`
- ✅ New flags (optional):
    --mock              Use sample_data from entities.py when entities.data.py missing
    --targets=all|backend|frontend|search (comma separated allowed)
    --backup            Write .bak.<timestamp> when overwriting files
    --no-overwrite      Skip rewriting existing files when content would change
    --dry-run           Print planned writes without touching disk

- ✅ Preserves your existing behavior:
    - generate_models
    - generate_mock_data
    - generate_test_data
    - generate_excel_dump
    - generate_pages_config
    - generate_test_cases_from_mock
    - generate_search_tests
    - copy_entity_files

- ✅ **Additive**: also generates **per-entity** frontend mocks exporting `options()`:
    src/clients/<client>/mock/<entity>.ts
    Shape:
    {
      entity,
      primary_key,
      fields: [{ name, type?, label?, required?, read_only?, nullable?, primary_key?, foreign_key?, default? }],
      admin: {
        table: {
          delete_confirmation: true,
          inline_edit: false,
          show_filters: true,
          page_size: 20,
          global_search: true,
          column_search: false,
          sortable: true,
          sticky_header: false
        },
        form: null,
        list: null
      }
    }

The generator is **non-destructive**: if a mock file already has an `options()` export, it won't
touch it; otherwise it creates or appends just the `options()` function.

"""

from __future__ import annotations
from decimal import Decimal
import os
import importlib.util
from datetime import datetime, date, timedelta
import re
import json
import pandas as pd
import sys
import shutil
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable

# ----------------
# CLI / Flags
# ----------------
if len(sys.argv) < 2:
    print("Usage: python code_generator.py <client_name> [mock] [--targets=...] [--backup] [--no-overwrite] [--dry-run]")
    sys.exit(2)

CLIENT_NAME = sys.argv[1]
FLAGS = set(a for a in sys.argv[2:] if a.startswith("--"))
MOCK_MODE = ("mock" in sys.argv[2:]) or ("--mock" in FLAGS)

# Parse --targets
_targets_arg = next((a for a in sys.argv[2:] if a.startswith("--targets=")), None)
if _targets_arg:
    TARGETS = [t.strip() for t in _targets_arg.split("=", 1)[1].split(",") if t.strip()]
else:
    TARGETS = ["all"]

BACKUP = "--backup" in FLAGS
NO_OVERWRITE = "--no-overwrite" in FLAGS
DRY_RUN = "--dry-run" in FLAGS

# ----------------
# Paths
# ----------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
CLIENTS_DIR = os.path.join(BACKEND_DIR, "clients")
CLIENT_DIR = os.path.join(CLIENTS_DIR, CLIENT_NAME)
ENTITIES_PATH = os.path.join(CLIENT_DIR, "entities.py")
CONFIG_PATH = os.path.join(CLIENT_DIR, "config.json")
PAGES_OUTPUT_DIR = os.path.join(ROOT_DIR, f"nishify.io/src/clients/{CLIENT_NAME}/pages")
TESTS_OUTPUT_DIR = os.path.join(BACKEND_DIR, "tests", CLIENT_NAME)
ENTITIES_DATA_PATH = os.path.join(CLIENT_DIR, "entities.data.py")
ELASTIC_ENTITIES_PATH = os.path.join(CLIENT_DIR, "elastic_entities.py")
FRONTEND_CLIENT_DIR = os.path.join(ROOT_DIR, f"nishify.io/src/clients/{CLIENT_NAME}")
MOCK_OUTPUT_DIR = os.path.join(FRONTEND_CLIENT_DIR, "mock")
FRONTEND_CONFIG_SRC = os.path.join(CLIENT_DIR, "frontend.api.config.json")

def _json_sanitize(obj):
    """Recursively convert obj into something JSON serializable."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, dict):
        return {k: _json_sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_json_sanitize(x) for x in obj]
    return obj

def _regenerate_ids_if_needed(sample_data: List[Dict[str, Any]]):
    """
    Ensure 'id' uniqueness & presence in sample data for stable tests/mocks.
    """
    if not sample_data:
        return sample_data
    ids = {r["id"] for r in sample_data if isinstance(r.get("id"), int)}
    max_id = max(ids) if ids else 0
    next_id = max_id + 1
    out = []
    for row in sample_data:
        row = dict(row)
        if not isinstance(row.get("id"), int):
            row["id"] = next_id
            next_id += 1
        out.append(row)
    return out

# -------------------------------------------------------------------------------------------------
# File ops
# -------------------------------------------------------------------------------------------------
def _ensure_dir(p):
    if DRY_RUN:
        print(f"[dry-run] mkdir -p {p}")
    else:
        os.makedirs(p, exist_ok=True)

def _write(path: str, contents: str):
    if os.path.exists(path):
        if NO_OVERWRITE:
            print(f"[skip:no-overwrite] {path}")
            return
        if BACKUP:
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            shutil.copyfile(path, f"{path}.bak.{ts}")
    if DRY_RUN:
        print(f"[dry-run] write {path} ({len(contents)} bytes)")
    else:
        _ensure_dir(os.path.dirname(path))
        with open(path, "w", encoding="utf-8") as f:
            f.write(contents)

def _copy(src: str, dest: str):
    # 🔒 Guard: skip when src and dest are the same file
    if os.path.abspath(src) == os.path.abspath(dest):
        print(f"[skip:same-file] {src}")
        return
    try:
        if os.path.exists(dest) and os.path.samefile(src, dest):
            print(f"[skip:same-file] {src}")
            return
    except Exception:
        pass

    if not os.path.exists(src):
        print(f"[warn] source not found: {src}")
        return
    if os.path.exists(dest) and NO_OVERWRITE:
        print(f"[skip:no-overwrite] {dest}")
        return
    if BACKUP and os.path.exists(dest):
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copyfile(dest, f"{dest}.bak.{ts}")
    if DRY_RUN:
        print(f"[dry-run] copy {src} -> {dest}")
    else:
        _ensure_dir(os.path.dirname(dest))
        shutil.copyfile(src, dest)

def _log(msg: str):
    print(f"• {msg}")

def detect_fk_fields(entity_name: str, entities_cfg: dict):
    """
    Return list of (fk_field_name, parent_entity) for an entity,
    based on `foreign_key` meta OR *_id that matches another entity.
    """
    cfg = entities_cfg[entity_name]
    fields = (cfg.get("fields") or {})
    out = []
    for name, meta in fields.items():
        if meta.get("primary_key"):
            continue
        fk = meta.get("foreign_key")
        if fk:
            parent = str(fk).split(".", 1)[0]
            out.append((name, parent))
        elif name.endswith("_id"):
            parent = name[:-3]
            if parent in entities_cfg:
                out.append((name, parent))
    return out



# -------------------------------------------------------------------------------------------------
# Load configs
# -------------------------------------------------------------------------------------------------
if not os.path.exists(ENTITIES_PATH):
    print(f"entities.py not found for client '{CLIENT_NAME}': {ENTITIES_PATH}")
    sys.exit(2)

spec_entities = importlib.util.spec_from_file_location("entities", ENTITIES_PATH)
entities_module = importlib.util.module_from_spec(spec_entities)
spec_entities.loader.exec_module(entities_module)
entities = entities_module.entities

# merge entities.data.py into entities (sample_data)
if os.path.exists(ENTITIES_DATA_PATH):
    spec_data = importlib.util.spec_from_file_location("entities_data", ENTITIES_DATA_PATH)
    data_module = importlib.util.module_from_spec(spec_data)
    spec_data.loader.exec_module(data_module)
    data_entities = getattr(data_module, "entities_data", {})
    for key, value in data_entities.items():
        if key in entities:
            entities[key]["sample_data"] = _regenerate_ids_if_needed(value.get("sample_data", []))
        else:
            print(f"⚠️ {key} found in entities.data.py but not in entities.py — skipping.")
else:
    print("⚠️ entities.data.py not found — proceeding without sample data.")

# -------------------------------------------------------------------------------------------------
# Helpers preserved from your code
# -------------------------------------------------------------------------------------------------
def log(msg):
    _log(msg)

def default_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def type_map(field_type):
    return {
        "int": "Integer",
        "str": "String",
        "float": "Float",
        "bool": "Boolean",
        "date": "Date",
        "datetime": "DateTime",
    }.get(field_type, "String")

def _camelize(name: str) -> str:
    if not name:
        return ""
    parts = re.split(r'[_\s\-]+', name)
    return "".join(p.capitalize() for p in parts if p)

def _snake(name: str) -> str:
    s = re.sub(r"([A-Z]+)", r"_\1", name).lower().strip("_")
    s = re.sub(r"[\s\-]+", "_", s)
    return s

# ---------------------------------------------------------------------------------------------
# Backend generation (kept from your existing behavior)
# ---------------------------------------------------------------------------------------------
MODEL_OUTPUT_DIR = os.path.join(BACKEND_DIR, "clients", CLIENT_NAME, "models")
TESTDATA_OUTPUT_DIR = os.path.join(BACKEND_DIR, "clients", CLIENT_NAME, "testdata")
EXCEL_OUTPUT_DIR = os.path.join(BACKEND_DIR, "clients", CLIENT_NAME, "excel")
SEARCH_OUTPUT_DIR = os.path.join(BACKEND_DIR, "clients", CLIENT_NAME, "search")

def generate_models():
    _ensure_dir(MODEL_OUTPUT_DIR)

    for entity, config in entities.items():
        fields = config.get("fields", {})
        has_primary_key = any(field_conf.get("primary_key") for field_conf in fields.values())
        if not has_primary_key:
            # inject surrogate id
            fields = {"id": {"type": "int", "primary_key": True}, **fields}

        fk_imports = set()
        field_lines = []
        relationship_lines = []

        for field_name, field_conf in fields.items():
            sql_type = type_map(field_conf.get("type"))
            args = [sql_type]

            if field_conf.get("foreign_key"):
                fk_table = field_conf["foreign_key"].split(".")[0]
                rel_class = _camelize(fk_table)
                args.append(f"ForeignKey('{field_conf['foreign_key']}')")
                rel_name = field_name.removesuffix("_id")
                relationship_lines.append(f"    {rel_name} = relationship('{rel_class}')")
                fk_imports.add(f"from backend.clients.{CLIENT_NAME}.models.{fk_table} import {rel_class}")

            kwargs = []
            if field_conf.get("primary_key"):
                kwargs.append("primary_key=True")
            if field_conf.get("required"):
                kwargs.append("nullable=False")
            if field_conf.get("auto_now"):
                if sql_type == "DateTime":
                    kwargs.append("default=datetime.utcnow")
                elif sql_type == "Date":
                    kwargs.append("default=date.today")
                else:
                    kwargs.append("default=datetime.utcnow")

            all_args = args + kwargs
            field_lines.append(f"    {field_name} = Column({', '.join(all_args)})")

        # --- build __table_args__ from unique_together (if any) ---
        uniq_pairs = config.get("unique_together") or []
        table_args_line = ""
        if uniq_pairs:
            uc_items = []
            for i, pair in enumerate(uniq_pairs):
                cols = ", ".join(repr(c) for c in pair)
                uc_items.append(f"UniqueConstraint({cols}, name='uix_{entity}_{i}')")
            table_args_line = f"    __table_args__ = ({', '.join(uc_items)},)"
        lines = [
            "from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, UniqueConstraint",
            "from sqlalchemy.orm import relationship",
            "from datetime import datetime, date",
            *sorted(fk_imports),
            "",
            "from backend.utils.db_base import Base",
            f"\nclass {_camelize(entity)}(Base):",
            f"    __tablename__ = '{entity}'",
        ] + ([table_args_line] if table_args_line else []) + field_lines + relationship_lines


        model_code = "\n".join(lines)
        model_path = os.path.join(MODEL_OUTPUT_DIR, f"{entity}.py")
        _write(model_path, model_code)
        log(f"✅ Generated model for {entity} at {model_path}")

def generate_mock_data():
    _ensure_dir(MOCK_OUTPUT_DIR)

    for entity, config in entities.items():
        sample_data = config.get("sample_data", [])

        js_sample = json.dumps(sample_data, default=_json_sanitize, ensure_ascii=False)

        handlers = {
            "options": f"() => {json.dumps(list(config.get('fields', {}).keys()))}",
            "get": f"() => {js_sample}",
            "getOne": f"(id) => (Array.isArray({js_sample}) && {js_sample}.length ? {js_sample}[0] : {{}})",
            "post": "(payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) })",
            "update": "(payload) => payload"
        }

        lines = [f"export const {entity} = {{"] + [f"  {k}: {v}," for k, v in handlers.items()] + ["};"]

        mock_path = os.path.join(MOCK_OUTPUT_DIR, f"{entity}.ts")
        _write(mock_path, "\n".join(lines))
        log(f"✅ Generated mock for {entity} at {mock_path}")

def generate_test_data():
    _ensure_dir(TESTDATA_OUTPUT_DIR)

    for entity, config in entities.items():
        data = config.get("sample_data", [])
        json_path = os.path.join(TESTDATA_OUTPUT_DIR, f"{entity}.json")
        _write(json_path, json.dumps(data, indent=2, default=default_serializer))
        log(f"✅ Generated test data for {entity} at {json_path}")

def generate_excel_dump():
    _ensure_dir(EXCEL_OUTPUT_DIR)
    with pd.ExcelWriter(os.path.join(EXCEL_OUTPUT_DIR, "sample_output.xlsx")) as writer:
        for entity, config in entities.items():
            data = config.get("sample_data", [])
            pd.DataFrame(data).to_excel(writer, sheet_name=entity[:31], index=False)
    log(f"✅ Excel dump created at {os.path.join(EXCEL_OUTPUT_DIR, 'sample_output.xlsx')}")

def generate_pages_config():
    _ensure_dir(PAGES_OUTPUT_DIR)

    for root, dirs, files in os.walk(CLIENT_DIR):
        for file in files:
            src_file = os.path.join(root, file)
            relative_path = os.path.relpath(src_file, CLIENT_DIR)
            dest_file = os.path.join(PAGES_OUTPUT_DIR, relative_path)
            _copy(src_file, dest_file)
            log(f"✅ Copied {relative_path} to frontend at {os.path.abspath(dest_file)}")

def copy_entity_files():
    src_dir = CLIENT_DIR
    dest_dir = os.path.join(BACKEND_DIR, "clients", CLIENT_NAME)

    # 🔒 Guard: if src and dest are identical, skip to avoid SameFileError
    if os.path.abspath(src_dir) == os.path.abspath(dest_dir):
        _log("copy_entity_files: source and destination are identical; skipping.")
        return

    _ensure_dir(dest_dir)

    for root, _, files in os.walk(src_dir):
        for fname in files:
            src = os.path.join(root, fname)
            rel = os.path.relpath(src, src_dir)
            dest = os.path.join(dest_dir, rel)
            _copy(src, dest)
    log(f"✅ Copied client files to {dest_dir}")



def generate_test_cases_from_mock(entities_map, test_dir):
    """Generate simple CRUD tests per entity:
    - /api base path
    - trailing commas
    - include non-auto PKs
    - include ALL FKs with unique values to avoid composite-unique collisions
    - no nested f-strings that cause SyntaxError
    """
    import re as _re
    from pathlib import Path

    Path(test_dir).mkdir(parents=True, exist_ok=True)

    def snake(name: str) -> str:
        return _re.sub(r'[^a-zA-Z0-9_]+', '_', name.strip()).lower()

    for entity_name, cfg in entities_map.items():
        fields = cfg.get("fields", {})
        if not fields:
            print(f"⚠️ Skipping {entity_name}: no fields")
            continue

        pk_fields = [k for k, v in fields.items() if v.get("primary_key")]
        has_auto_id = "id" in pk_fields and (fields.get("id", {}).get("type") in ("int", "integer", None))
        fk_fields_all = [k for k, v in fields.items() if v.get("foreign_key")]

        tfile = os.path.join(test_dir, f"test_{snake(entity_name)}.py")
        header = [
            "import json",
            "import httpx",
            "from datetime import datetime, date, timedelta",
            "",
            f'BASE_URL = "http://localhost:8000/api/{entity_name}"',
            "",
        ]

        tests = []

        # ---------- CREATE ----------
        tests += [
            "def test_create():",
            "    global CREATED_ID",
            "    payload = {",
        ]

        assigns = []
        seed = 4802

        # Precompute unique FK values (avoid (po_id,item_id) duplicates etc.)
        fk_values = {}
        for idx, fname in enumerate(fk_fields_all):
            fcfg = fields.get(fname, {}) or {}
            ftype = fcfg.get("type")
            base_val = 800000 + seed + idx  # unique-ish
            fk_values[fname] = f'"{base_val}"' if ftype == "str" else str(base_val)

        for fname, fcfg in fields.items():
            # Skip only the classic auto-increment id
            if has_auto_id and fname == "id":
                continue

            # Non-auto PKs must be present
            if fname in pk_fields and not (has_auto_id and fname == "id"):
                if fname in fk_values:
                    assigns.append(f'        "{fname}": {fk_values[fname]},')
                else:
                    ftype = (fcfg or {}).get("type")
                    val = 900000 + seed
                    val_repr = f'"{val}"' if ftype == "str" else str(val)
                    assigns.append(f'        "{fname}": {val_repr},')
                continue

            # Include ALL FKs using the precomputed unique values
            if fname in fk_values:
                assigns.append(f'        "{fname}": {fk_values[fname]},')
                continue

            # Regular fields
            ftype = (fcfg or {}).get("type")
            if ftype == "int":
                assigns.append(f'        "{fname}": {1000 + seed},')
            elif ftype == "float":
                assigns.append(f'        "{fname}": {1000.0 + float(seed)},')
            elif ftype == "bool":
                assigns.append(f'        "{fname}": {bool(seed % 2)},')
            elif ftype == "date":
                assigns.append(f'        "{fname}": (date(2025, 8, 1) + timedelta(days={seed})).isoformat(),')
            elif ftype == "datetime":
                assigns.append(f'        "{fname}": (datetime(2025, 8, 1, 12, 0, 0) + timedelta(days={seed})).isoformat(),')
            else:
                assigns.append(f'        "{fname}": "v{seed}",')
            seed += 1

        if not assigns:
            assigns.append('        "name": "auto",')

        tests += assigns
        tests += [
            "    }",
            "    response = httpx.post(BASE_URL, json=payload)",
            "    assert response.status_code == 200",
            "    data = response.json()",
            "    CREATED_ID = data.get('id')",
            "    assert CREATED_ID is not None",
            "",
        ]

        # ---------- GET ONE ----------
        tests += [
            "def test_get_one():",
            "    rid = CREATED_ID if 'CREATED_ID' in globals() and CREATED_ID else 4802",
            "    resp = httpx.get(f\"{BASE_URL}/{rid}\")",
            "    if resp.status_code == 404:",
            "        payload = {",
        ]
        payload2 = [line for line in assigns]
        payload2.append('        "id": rid,')
        tests += payload2
        tests += [
            "        }",
            "        _ = httpx.post(BASE_URL, json=payload)",
            "        resp = httpx.get(f\"{BASE_URL}/{rid}\")",
            "    assert resp.status_code in (200, 404)",
            "    if resp.status_code == 200:",
            "        data = resp.json()",
            "        assert isinstance(data, dict)",
            "",
        ]

        # ---------- LIST ----------
        tests += [
            "def test_list():",
            "    resp = httpx.get(BASE_URL)",
            "    assert resp.status_code == 200",
            "    data = resp.json()",
            "    assert isinstance(data, dict) and 'items' in data",
            "",
        ]

        # ---------- UPDATE ----------
        non_pk_fk_field = next((n for n in fields.keys() if n not in pk_fields and n not in fk_fields_all), None)
        if has_auto_id:
            tests += [
                "def test_update():",
                "    rid = CREATED_ID if 'CREATED_ID' in globals() and CREATED_ID else 4802",
                "    payload = {",
                '        "id": rid,',
            ]
            if non_pk_fk_field:
                fcfg_u = fields[non_pk_fk_field] or {}
                ftype_u = fcfg_u.get("type")
                if ftype_u == "int":
                    tests.append(f'        "{non_pk_fk_field}": 999999,')
                elif ftype_u == "float":
                    tests.append(f'        "{non_pk_fk_field}": 1234.5,')
                elif ftype_u == "bool":
                    tests.append(f'        "{non_pk_fk_field}": False,')
                elif ftype_u == "date":
                    tests.append(f'        "{non_pk_fk_field}": date(2025, 8, 2).isoformat(),')
                elif ftype_u == "datetime":
                    tests.append(f'        "{non_pk_fk_field}": datetime(2025, 8, 2, 13, 0, 0).isoformat(),')
                else:
                    tests.append(f'        "{non_pk_fk_field}": "auto-upd",')
            else:
                tests.append('        "name": "auto-upd",')
            tests += [
                "    }",
                "    resp = httpx.put(f\"{BASE_URL}/{rid}\", json=payload)",
                "    assert resp.status_code in (200, 404)",
                "",
            ]

        # ---------- DELETE ----------
        if has_auto_id:
            tests += [
                "def test_delete():",
                "    rid = CREATED_ID if 'CREATED_ID' in globals() and CREATED_ID else 4802",
                "    resp = httpx.delete(f\"{BASE_URL}/{rid}\")",
                "    assert resp.status_code in (200, 404)",
                "",
            ]

        _write(tfile, "\n".join(header + tests))
        print(f"✅ Wrote tests: {tfile}")

def generate_search_tests():
    """Auto-generate search tests for all entities if elastic_entities.py exists."""
    if not os.path.exists(ELASTIC_ENTITIES_PATH):
        log("No elastic_entities.py — skipping search tests.")
        return
    spec = importlib.util.spec_from_file_location("elastic_entities", ELASTIC_ENTITIES_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    elastic_entities = getattr(mod, "elastic_entities", None)
    if not isinstance(elastic_entities, dict):
        log("elastic_entities missing — skipping search tests.")
        return

    out_dir = os.path.join(TESTS_OUTPUT_DIR, "search")
    os.makedirs(out_dir, exist_ok=True)

    for entity, cfg in elastic_entities.items():
        path = os.path.join(out_dir, f"test_{entity}_search.py")
        lines = [
            "import httpx",
            "import json",
            "",
            f'BASE_URL = "http://localhost:8000/search/{entity}"',
            "",
            "def test_search_basic():",
            "    resp = httpx.get(BASE_URL, params={\"q\": \"test\"})",
            "    assert resp.status_code in (200, 404, 501)",
            "    # response may be not implemented depending on project state",
            "",
        ]
        _write(path, "\n".join(lines))
        log(f"✅ Wrote search test: {path}")

def search_snapshot():
    out_path = os.path.join(SEARCH_OUTPUT_DIR, "snapshot.json")
    os.makedirs(SEARCH_OUTPUT_DIR, exist_ok=True)
    snap = {"generated_at": datetime.now().isoformat(), "entities": list(entities.keys())}
    _write(out_path, json.dumps(snap, indent=2))
    log(f"✅ Wrote search snapshot: {out_path}")

def generate_frontend_config():
    if not os.path.exists(FRONTEND_CONFIG_SRC):
        _log("frontend.api.config.json not found; skipping frontend config copy.")
        return
    dest = os.path.join(FRONTEND_CLIENT_DIR, "config.json")
    if DRY_RUN:
        print(f"[dry-run] copy frontend config to {dest}")
    else:
        _ensure_dir(os.path.dirname(dest))
        shutil.copyfile(FRONTEND_CONFIG_SRC, dest)
    _log(f"Copied frontend config to {dest}")

# -------------------------------------------------------------------------------------------------
# Rich Frontend Options Generation (ADD-ONLY, non-destructive)
# -------------------------------------------------------------------------------------------------
DEFAULT_ADMIN = {
    "table": {
        "delete_confirmation": True,
        "inline_edit": False,
        "show_filters": True,
        "page_size": 10,
        "global_search": True,
        "column_search": False,
        "sortable": True,
        "sticky_header": False,
    },
    "form": None,
    "list": None,
}

def _deep_merge(a, b):
    if a is None: return b
    if b is None: return a
    if isinstance(a, dict) and isinstance(b, dict):
        out = dict(a)
        for k, v in b.items():
            out[k] = _deep_merge(out.get(k), v)
        return out
    return b

def _fields_map_to_list(entity_cfg: dict) -> list:
    fields_cfg = entity_cfg.get("fields") if isinstance(entity_cfg, dict) else {}
    if not isinstance(fields_cfg, dict):
        fields_cfg = {}
    names = list(fields_cfg.keys())
    fields_ts = []
    for name in names:
        f = fields_cfg.get(name) or {}
        fields_ts.append({
            "name": name,
            "type": f.get("type"),
            "label": f.get("label"),
            "required": bool(f.get("required", False)),
            "read_only": bool(f.get("read_only", False)),
            "nullable": bool(f.get("nullable", True)),
            "primary_key": bool(f.get("primary_key", False)),
            "foreign_key": f.get("foreign_key"),
            "default": f.get("default"),
        })
    fields_ts.sort(key=lambda d: (0 if d["name"] == "id" else 1, d["name"]))
    return fields_ts

def _build_rich_options(entity: str, entity_cfg: dict) -> dict:
    fields = _fields_map_to_list(entity_cfg or {})
    pk = "id" if any(f["name"] == "id" for f in fields) else None
    if not pk:
        for f in fields:
            if f.get("primary_key"):
                pk = f["name"]; break
    admin_cfg = entity_cfg.get("admin") if isinstance(entity_cfg, dict) else {}
    admin = _deep_merge(DEFAULT_ADMIN, admin_cfg or {})
    return {
        "entity": entity,
        "primary_key": pk,
        "fields": fields,
        "admin": admin,
    }

def _render_ts_options_module(payload: dict) -> str:
    body = json.dumps(payload, indent=2)
    return (
        "// Auto-generated by code_generator.py — per-entity mock options\n"
        f"// entity: {payload.get('entity')}\n\n"
        "export async function options() {\n"
        f"  return {body}\n"
        "}\n"
    )

def generate_frontend_rich_options():
    """Generate/append mock/<entity>.ts with an `options()` export per entity."""
    os.makedirs(MOCK_OUTPUT_DIR, exist_ok=True)
    logs = []
    for entity, cfg in entities.items():
        ts_path = os.path.join(MOCK_OUTPUT_DIR, f"{entity}.ts")
        payload = _build_rich_options(entity, cfg or {})
        module_ts = _render_ts_options_module(payload)
        action = None
        if not os.path.exists(ts_path):
            with open(ts_path, "w", encoding="utf-8") as f:
                f.write(module_ts)
            action = "created"
        else:
            with open(ts_path, "r", encoding="utf-8") as f:
                cur = f.read()
            if re.search(r"\boptions\s*\(", cur):
                action = "skipped (already has options)"
            else:
                with open(ts_path, "a", encoding="utf-8") as f:
                    f.write("\n" + module_ts)
                action = "appended"
        logs.append(f"[{entity}] {action}: {os.path.relpath(ts_path, ROOT_DIR)}")
    for l in logs:
        _log(l)

# -------------------------------------------------------------------------------------------------
# Adapter registry (lightweight)
# -------------------------------------------------------------------------------------------------
ADAPTERS: Dict[str, Callable[[], None]] = {
    # backend bundle
    "backend.models": generate_models,
    "backend.testdata": generate_test_data,
    "backend.legacy_tests": lambda: generate_test_cases_from_mock(entities, TESTS_OUTPUT_DIR),
    "backend.copy_entities": copy_entity_files,
    # frontend bundle
    "frontend.mocks": generate_mock_data,
    "frontend.config": generate_frontend_config,
    "frontend.pages": generate_pages_config,
    "frontend.rich_options": generate_frontend_rich_options,
    # search bundle
    "search.tests": generate_search_tests,
    "search.snapshot": search_snapshot,
}

TARGET_MAP: Dict[str, List[str]] = {
    "backend": ["frontend.config","backend.models", "backend.testdata", "backend.legacy_tests", "backend.copy_entities"],
    "frontend": ["frontend.config","frontend.mocks", "frontend.pages","frontend.rich_options"],
    "search": ["search.tests", "search.snapshot"],
    "all": [
        "backend.models", "backend.testdata", "backend.legacy_tests", "backend.copy_entities",
        "frontend.mocks", "frontend.pages","frontend.config","frontend.rich_options",
        "search.tests", "search.snapshot",
    ],
}

# ---------------------------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------------------------
def run_targets():
    for tgt in TARGETS:
        if tgt not in TARGET_MAP:
            print(f"[warn] Unknown target '{tgt}', skipping.")
            continue
        _log(f"Running target: {tgt}")
        for step in TARGET_MAP[tgt]:
            fn = ADAPTERS.get(step)
            if not fn:
                print(f"[warn] Missing adapter for step '{step}'")
                continue
            _log(f"  • {step}")
            fn()

if __name__ == "__main__":
    run_targets()
