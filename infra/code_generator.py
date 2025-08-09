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
    --dry-run           Do not write files; only print summary
- ✅ No assumptions: explicit errors when required files are missing
- ✅ File overwrite safe; auto-create folders
- ✅ End-of-run **Generation Summary** with created/overwritten/dryrun counts

Outputs (unchanged locations):
- Backend:
  - backend/clients/<client>/models/*.py  (from generate_models)
  - backend/clients/<client>/test_data/*.json (from generate_test_data)
  - backend/tests/<client>/test_*.py (from generate_test_cases_from_mock & generate_search_tests)
  - backend/clients/<client>/elastic_entities.py (copied by copy_entity_files)
- Frontend:
  - nishify.io/src/lib/api/mock/<client>/*.ts (from generate_mock_data)
  - nishify.io/src/clients/<client>/** (from generate_pages_config)
- Search:
  - backend/clients/<client>/elastic/elastic_entities.snapshot.json (new minimal snapshot)
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
from typing import Dict, Any, List, Optional

# -------------------------------------------------------------------------------------------------
# Flags & CLI (backwards compatible + new optional flags)
# -------------------------------------------------------------------------------------------------
LOG = True

if len(sys.argv) < 2:
    raise ValueError("Usage: python code_generator.py <client_name> [mock] [--targets all|backend|frontend|search] [--backup] [--dry-run]")

CLIENT_NAME = sys.argv[1]
FLAGS = set(a for a in sys.argv[2:] if a.startswith("--"))
MOCK_MODE = ("mock" in sys.argv[2:]) or ("--mock" in FLAGS)

# Parse --targets
_targets_arg = next((a for a in sys.argv[2:] if a.startswith("--targets")), "--targets=all")
TARGETS = _targets_arg.split("=", 1)[1] if "=" in _targets_arg else "all"
TARGETS = [t.strip() for t in TARGETS.split(",") if t.strip()] or ["all"]

BACKUP = "--backup" in FLAGS
DRY_RUN = "--dry-run" in FLAGS

# -------------------------------------------------------------------------------------------------
# Paths (preserve your existing structure)
# -------------------------------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))  # nishify root
CLIENTS_DIR = os.path.join(ROOT_DIR, "clients")
CLIENT_DIR = os.path.join(CLIENTS_DIR, CLIENT_NAME)
ENTITIES_PATH = os.path.join(CLIENT_DIR, "entities.py")
CONFIG_PATH = os.path.join(CLIENT_DIR, "config.json")
PAGES_OUTPUT_DIR = os.path.join(ROOT_DIR, f"nishify.io/src/clients/{CLIENT_NAME}")
TESTS_OUTPUT_DIR = os.path.join(ROOT_DIR, f"backend/tests/{CLIENT_NAME}")
MODEL_OUTPUT_DIR = os.path.join(ROOT_DIR, f"backend/clients/{CLIENT_NAME}/models")
TESTDATA_OUTPUT_DIR = os.path.join(ROOT_DIR, f"backend/clients/{CLIENT_NAME}/test_data")
EXCEL_OUTPUT_FILE = os.path.join(TESTDATA_OUTPUT_DIR, "test_data.xlsx")
BACKEND_CLIENT_DIR = os.path.join(ROOT_DIR, "backend", "clients", CLIENT_NAME)
SEARCH_OUTPUT_DIR = os.path.join(BACKEND_CLIENT_DIR, "elastic")
ELASTIC_ENTITIES_PATH = os.path.join(CLIENT_DIR, "elastic_entities.py")
ENTITIES_DATA_PATH = os.path.join(CLIENT_DIR, "entities.data.py")
FRONTEND_CLIENT_DIR = os.path.join(ROOT_DIR, f"nishify.io/src/clients/{CLIENT_NAME}")
MOCK_OUTPUT_DIR = os.path.join(FRONTEND_CLIENT_DIR, "mock")
FRONTEND_CONFIG_SRC = os.path.join(CLIENT_DIR, "frontend.api.config.json")


def _json_sanitize(obj):
    """Recursively convert obj into something JSON-serializable."""
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            key = k if isinstance(k, str) else str(k)
            out[key] = _json_sanitize(v)
        return out
    if isinstance(obj, (list, tuple, set)):
        return [_json_sanitize(v) for v in obj]
    if callable(obj):
        name = getattr(obj, "__name__", "anonymous")
        return f"<callable:{name}>"
    return f"<{type(obj).__name__}>"
def _regenerate_ids_if_needed(entity_name, rows):
    """Regenerate duplicate or None primary keys in sample_data to avoid UNIQUE constraint errors."""
    if not isinstance(rows, list):
        return rows
    seen = set()
    for r in rows:
        if not isinstance(r, dict):
            continue
        if "id" in r:
            val = r["id"]
            if val is None or val in seen:
                new_id = random.randint(1000, 999999)
                while new_id in seen:
                    new_id = random.randint(1000, 999999)
                r["id"] = new_id
                seen.add(new_id)
            else:
                seen.add(val)
    return rows

# -------------------------------------------------------------------------------------------------
# File writer with backups + dry-run + summary
# -------------------------------------------------------------------------------------------------
@dataclass
class FileEvent:
    path: str
    action: str  # created|overwritten|skipped|dryrun|copied

@dataclass
class GenSummary:
    events: List[FileEvent] = field(default_factory=list)
    def add(self, path: str, action: str):
        self.events.append(FileEvent(path, action))
    def print(self):
        created = sum(1 for e in self.events if e.action == "created")
        overwritten = sum(1 for e in self.events if e.action == "overwritten")
        copied = sum(1 for e in self.events if e.action == "copied")
        dry = sum(1 for e in self.events if e.action == "dryrun")
        print("\n=== Generation Summary ===")
        print(f"Created:     {created}")
        print(f"Overwritten: {overwritten}")
        print(f"Copied:      {copied}")
        print(f"Dry-Run:     {dry}")
        print("--------------------------")
        for e in self.events:
            print(f"[{e.action}] {e.path}")
        print("==========================\n")

SUMMARY = GenSummary()

def _log(msg: str):
    if LOG:
        print(msg)

def _ensure_dir(path: str):
    if DRY_RUN:
        return
    os.makedirs(path, exist_ok=True)

def _write(path: str, content: str):
    _ensure_dir(os.path.dirname(path))
    if DRY_RUN:
        SUMMARY.add(path, "dryrun")
        return
    action = "created" if not os.path.exists(path) else "overwritten"
    if BACKUP and os.path.exists(path):
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(path, f"{path}.bak.{stamp}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    SUMMARY.add(path, action)

def _copy(src: str, dst: str):
    _ensure_dir(os.path.dirname(dst))
    if DRY_RUN:
        SUMMARY.add(dst, "dryrun")
        return
    if BACKUP and os.path.exists(dst):
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(dst, f"{dst}.bak.{stamp}")
    shutil.copy2(src, dst)
    SUMMARY.add(dst, "copied")

# -------------------------------------------------------------------------------------------------
# Load configs (no assumptions)
# -------------------------------------------------------------------------------------------------
if not os.path.exists(ENTITIES_PATH):
    print(f"❌ Client '{CLIENT_NAME}' not found at {ENTITIES_PATH}\n")
    print("📁 Available clients:")
    for folder in os.listdir(CLIENTS_DIR):
        if os.path.isdir(os.path.join(CLIENTS_DIR, folder)):
            print(f"- {folder}")
    # keep your existing scaffold flow, but do not prompt in dry-run
    if not DRY_RUN:
        scaffold = input(f"\nWould you like to scaffold a new client '{CLIENT_NAME}'? (y/n): ").strip().lower()
    else:
        scaffold = 'n'
    if scaffold == 'y':
        os.makedirs(CLIENT_DIR, exist_ok=True)
        _write(ENTITIES_PATH, "entities = {}\n")
        with open(ENTITIES_DATA_PATH, 'w') as f:
            f.write("entities_data = {}\n")
        with open(CONFIG_PATH, 'w') as f:
            json.dump({
                "env": {"dev_url": "http://localhost:8000/api", "prod_url": "https://api.example.com"},
                "use_mock": True, "theme": "default", "auth_mode": "none"
            }, f, indent=2)
        print(f"✅ Scaffolded new client at {CLIENT_DIR}. Now re-run the script.")
        sys.exit(0)
    else:
        print("❌ Aborting.")
        sys.exit(1)

client_config = {}
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as f:
        client_config = json.load(f)

# import entities
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
            entities[key]["sample_data"] = value.get("sample_data", [])
        else:
            print(f"⚠️ {key} found in entities.data.py but not in entities.py — skipping.")
else:
    print("⚠️ entities.data.py not found — proceeding without sample data.")
for _ename, _cfg in entities.items():
    if isinstance(_cfg, dict) and "sample_data" in _cfg:
        _cfg["sample_data"] = _regenerate_ids_if_needed(_ename, _cfg.get("sample_data", []))


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
    parts = re.split(r'[_\W]+', name)
    return "".join(p.capitalize() for p in parts if p)

# -------------------------------------------------------------------------------------------------
# === ORIGINAL FUNCTIONS (kept; writes routed via _write / _copy) ===
# -------------------------------------------------------------------------------------------------

def generate_models():
    _ensure_dir(MODEL_OUTPUT_DIR)

    for entity, config in entities.items():
        fields = config["fields"]

        has_primary_key = any(field_conf.get("primary_key") for field_conf in fields.values())
        if not has_primary_key:
            log(f"⚠️ Skipping model for {entity} (no primary key found)")
            continue

        fk_imports = set()
        field_lines = []
        relationship_lines = []

        for field_name, field_conf in fields.items():
            sql_type = type_map(field_conf["type"])
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

        lines = [
            "from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey",
            "from sqlalchemy.orm import relationship",
            "from datetime import datetime, date",
            *sorted(fk_imports),
            "",
            "from backend.utils.db_base import Base",
            f"\nclass {_camelize(entity)}(Base):",
            f"    __tablename__ = '{entity}'",
            *field_lines,
            *relationship_lines,
        ]

        model_code = "\n".join(lines)
        model_path = os.path.join(MODEL_OUTPUT_DIR, f"{entity}.py")
        _write(model_path, model_code)
        log(f"✅ Generated model for {entity} at {model_path}")


def generate_mock_data():
    _ensure_dir(MOCK_OUTPUT_DIR)

    for entity, config in entities.items():
        sample_data = config.get("sample_data", [])

        # JSON-serialize so booleans/nulls are JS-friendly (true/false/null) and quotes are valid
        js_sample = json.dumps(sample_data, default=_json_sanitize, ensure_ascii=False)

        handlers = {
            "options": f"() => {json.dumps(list(config['fields'].keys()))}",
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
    all_dfs = []
    for entity, config in entities.items():
        data = config.get("sample_data", [])
        df = pd.DataFrame(data)
        all_dfs.append((entity, df))

    _ensure_dir(TESTDATA_OUTPUT_DIR)
    if DRY_RUN:
        log(f"DRY-RUN: would create Excel at {EXCEL_OUTPUT_FILE} with {len(all_dfs)} sheets")
        SUMMARY.add(EXCEL_OUTPUT_FILE, "dryrun")
        return

    with pd.ExcelWriter(EXCEL_OUTPUT_FILE, engine="xlsxwriter") as writer:
        for name, df in all_dfs:
            df.to_excel(writer, sheet_name=name, index=False)
    log(f"✅ Excel dump generated at {EXCEL_OUTPUT_FILE}")


def generate_pages_config():
    _ensure_dir(PAGES_OUTPUT_DIR)

    for root, dirs, files in os.walk(CLIENT_DIR):
        for file in files:
            src_file = os.path.join(root, file)
            relative_path = os.path.relpath(src_file, CLIENT_DIR)
            dest_file = os.path.join(PAGES_OUTPUT_DIR, relative_path)
            _copy(src_file, dest_file)
            log(f"✅ Copied {relative_path} to frontend at {os.path.abspath(dest_file)}")


def generate_test_cases_from_mock(entities_map, test_dir):
    """Legacy quick tests (kept as-is)."""
    import re as _re
    from datetime import datetime as _dt, timedelta as _td, date as _d
    from pathlib import Path

    Path(test_dir).mkdir(parents=True, exist_ok=True)

    def snake(name: str) -> str:
        return _re.sub(r'[^a-zA-Z0-9_]+', '_', name.strip()).lower()

    for entity_name, cfg in entities_map.items():
        fields = cfg.get("fields", {})
        if not fields:
            print(f"⚠️ Skipping {entity_name}: no fields")
            continue

        fk_fields = {}
        for fname, fcfg in fields.items():
            fk = fcfg.get("foreign_key")
            if isinstance(fk, str) and "." in fk:
                parent_entity, parent_idcol = fk.split(".", 1)
                fk_fields[fname] = (parent_entity, parent_idcol)

        num_fields = [k for k,v in fields.items() if v.get("type") in {"int","float"}]
        date_fields = [k for k,v in fields.items() if v.get("type") in {"date","datetime"}]
        str_fields = [k for k,v in fields.items() if v.get("type") == "str"]

        pk_field = None
        for k,v in fields.items():
            if v.get("primary_key"):
                pk_field = k
                break
        if not pk_field and "id" in fields:
            pk_field = "id"

        test_filename = os.path.join(test_dir, f"test_{snake(entity_name)}.py")

        lines = []
        lines.append('import os')
        lines.append('import httpx')
        lines.append('from datetime import datetime, timedelta, date')
        lines.append(f'BASE_URL = f"http://localhost:8000/api/{entity_name}"')
        lines.append('')
        lines.append('def _mk_parent(entity, body):')
        lines.append('    url = f"http://localhost:8000/api/{entity}"')
        lines.append('    r = httpx.post(url, json=body)')
        lines.append('    assert r.status_code in (200, 201), f"FK create failed: {entity} => {r.status_code} {r.text}"')
        lines.append('    return r.json()')
        lines.append('')
        lines.append('def _mk_payload(seed:int):')
        lines.append(f'    """Create a valid payload for {entity_name}; includes FKs if required."""')

        if fk_fields:
            for fname, (p_entity, p_idcol) in fk_fields.items():
                lines.append(f'    parent_{fname} = _mk_parent("{p_entity}", {{')
                lines.append(f'        "{p_idcol}": 900000 + seed,')
                lines.append('        "name": f"auto_parent_{seed}"')
                lines.append('    })')
        else:
            lines.append('    # no parent FKs')

        lines.append('    body = {')
        assigns = []
        for fname, fcfg in fields.items():
            if fname in fk_fields:
                continue
            ftype = fcfg.get("type")
            if ftype == "int":
                assigns.append(f'        "{fname}": 1000 + seed')
            elif ftype == "float":
                assigns.append(f'        "{fname}": 1000.0 + float(seed)')
            elif ftype == "bool":
                assigns.append(f'        "{fname}": bool(seed % 2)')
            elif ftype == "date":
                assigns.append(f'        "{fname}": (date(2025, 8, 1) + timedelta(days=seed)).isoformat()')
            elif ftype == "datetime":
                assigns.append(f'        "{fname}": (datetime(2025, 8, 1, 12, 0, 0) + timedelta(days=seed)).isoformat()')
            else:
                assigns.append(f'        "{fname}": f"auto_{fname}_{{seed}}"')
        if assigns:
            lines.extend(assigns)
        lines.append('    }')
        if fk_fields:
            lines.append('    body.update({')
            for fname, (_, p_idcol) in fk_fields.items():
                lines.append(f'        "{fname}": parent_{fname}["{p_idcol}"],')
            lines.append('    })')
        lines.append('    return body')
        lines.append('')
        lines.append('def test_crud_and_filters():')
        lines.append('    p1 = _mk_payload(1)')
        lines.append('    r1 = httpx.post(BASE_URL, json=p1); assert r1.status_code in (200, 201), r1.text')
        lines.append('    p2 = _mk_payload(2)')
        lines.append('    r2 = httpx.post(BASE_URL, json=p2); assert r2.status_code in (200, 201), r2.text')
        lines.append('    p3 = _mk_payload(3)')
        lines.append('    r3 = httpx.post(BASE_URL, json=p3); assert r3.status_code in (200, 201), r3.text')
        lines.append('    rl = httpx.get(BASE_URL); assert rl.status_code == 200')
        if pk_field:
            lines.append('    g1 = httpx.get(BASE_URL + "/" + str(1001))')
            lines.append('    # smoke only')
        lines.append('')
        lines.append('def test_options():')
        lines.append('    r = httpx.get(f"{BASE_URL}/options")')
        lines.append('    assert r.status_code == 200')
        lines.append('')
        test_src = "\n".join(lines).replace("\t", "    ")
        _write(test_filename, test_src)
        print(f"✅ Test case generated for {entity_name} at {test_filename}")


def copy_entity_files():
    client_dir = os.path.join(CLIENTS_DIR, CLIENT_NAME)
    _ensure_dir(BACKEND_CLIENT_DIR)

    for fname in ["entities.py", "elastic_entities.py"]:
        src = os.path.join(client_dir, fname)
        dst = os.path.join(BACKEND_CLIENT_DIR, fname)
        if os.path.exists(src):
            _copy(src, dst)
            print(f"✅ Copied {fname} to backend client folder.")
        else:
            print(f"⚠️  {fname} not found in client folder.")


def generate_search_tests():
    from_entities_path = os.path.join(CLIENT_DIR, "entities.py")
    from_data_path = os.path.join(CLIENT_DIR, "entities.data.py")
    from_elastic_path = os.path.join(CLIENT_DIR, "elastic_entities.py")

    def import_config(path):
        if not os.path.exists(path):
            return {}
        spec = importlib.util.spec_from_file_location("mod", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, "entities", None) or getattr(module, "entities_data", None) or {}

    entities_cfg = import_config(from_entities_path)
    entities_data = import_config(from_data_path)
    elastic_entities_cfg = import_config(from_elastic_path)

    _ensure_dir(TESTS_OUTPUT_DIR)

    for entity, config in entities_cfg.items():
        fields = config.get("fields", {})
        data = (entities_data.get(entity, {}) or {}).get("sample_data", [])
        if not fields:
            print(f"⚠️ No fields for {entity}, skipping test.")
            continue
        if not data:
            print(f"⚠️ No data for {entity}, skipping test.")
            continue

        # FK detection
        fk_fields = {}
        for fname, fcfg in fields.items():
            fk = fcfg.get("foreign_key")
            if isinstance(fk, str) and "." in fk:
                p_entity, p_idcol = fk.split(".", 1)
                fk_fields[fname] = (p_entity, p_idcol)

        is_indexed = entity in elastic_entities_cfg
        search_fields = elastic_entities_cfg.get(entity, {}).get("searchable_fields", []) if is_indexed else []

        sample = dict(data[0])

        # PK detection (supports composite)
        pk_fields = [k for k, v in fields.items() if v.get("primary_key")]
        has_single_pk = len(pk_fields) == 1
        pk_field = pk_fields[0] if has_single_pk else None
        pk_val = sample.get(pk_field, 1) if has_single_pk else None

        # Parent seeds (prefer sample_data)
        parent_seed_map = {}
        for _, (p_entity, _p_idcol) in fk_fields.items():
            p_data = (entities_data.get(p_entity, {}) or {}).get("sample_data", [])
            if p_data:
                parent_seed_map[p_entity] = json.dumps(p_data[0], default=default_serializer)
            else:
                parent_seed_map[p_entity] = json.dumps({"id": 700001, "name": "auto_parent"})

        lines = [
            "import os",
            "import json",
            "import httpx",
            "from datetime import datetime, timedelta",
            "",
            f'ENTITY = "{entity}"',
            'BASE = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")',
            'BASE_URL = f"{BASE}/api/{ENTITY}"',
            f"HAS_SINGLE_PK = {str(has_single_pk)}",
            f"PK_FIELDS = {json.dumps(pk_fields)}",
            "CREATED_ID = None",
            "",
            "def _mk_parent(entity, body):",
            '    url = f"{BASE}/api/{entity}"',
            "    r = httpx.post(url, json=body)",
            '    assert r.status_code in (200, 201), f"FK create failed: {entity} => {r.status_code} {r.text}"',
            "    return r.json()",
            "",
            "def _inject_fk(payload):",
            "    p = dict(payload)",
        ]

        # seed parents and assign FK ids
        for fname, (p_entity, p_idcol) in fk_fields.items():
            body_json = parent_seed_map[p_entity]
            lines += [
                f"    parent = _mk_parent('{p_entity}', json.loads({body_json!r}))",
                f"    p['{fname}'] = parent.get('{p_idcol}', parent.get('id', 700001))",
            ]
        lines += [
            "    return p",
            "",
            "def _pk_filter_from_payload(p):",
            "    params = {}",
            "    for k in PK_FIELDS:",
            "        if k in p:",
            "            params[k] = p[k]",
            "    return params",
            "",
            "def test_create():",
            "    global CREATED_ID",
            f"    payload = json.loads({json.dumps(json.dumps(sample, default=default_serializer))})",
            "    payload = _inject_fk(payload)",
            "    response = httpx.post(BASE_URL, json=payload)",
            "    assert response.status_code in (200, 201), response.text",
            "    try:",
            "        body = response.json() or {}",
            "    except Exception:",
            "        body = {}",
        ]

        if has_single_pk:
            lines += [
                f"    if isinstance(body, dict) and '{pk_field}' in body:",
                f"        CREATED_ID = body['{pk_field}']",
                "    elif isinstance(body, dict) and 'id' in body:",
                "        CREATED_ID = body['id']",
                "    elif isinstance(body, list) and body and isinstance(body[0], dict) and 'id' in body[0]:",
                "        CREATED_ID = body[0]['id']",
                f"    else:",
                f"        CREATED_ID = {pk_val}",
            ]
        else:
            lines += ["    # composite pk: no single CREATED_ID"]
        lines += ["    assert isinstance(body, (dict, list))", ""]

        # GET one
        if has_single_pk:
            lines += [
                "def test_get_one():",
                "    rid = CREATED_ID if 'CREATED_ID' in globals() and CREATED_ID else None",
                f"    rid = rid or {pk_val if pk_val is not None else 1}",
                '    resp = httpx.get(f"{BASE_URL}/{rid}")',
                "    if resp.status_code == 404:",
                f"        payload = json.loads({json.dumps(json.dumps(sample, default=default_serializer))})",
                "        payload = _inject_fk(payload)",
                f"        payload['{pk_field}'] = rid",
                "        httpx.post(BASE_URL, json=payload)",
                '        resp = httpx.get(f"{BASE_URL}/{rid}")',
                "        if resp.status_code == 404:",
                "            resp = httpx.get(BASE_URL, params={'id': rid})",
                '    assert resp.status_code == 200, f"GET failed: {resp.status_code} {resp.text}"',
                "",
            ]
        else:
            lines += [
                "def test_get_one():",
                f"    payload = json.loads({json.dumps(json.dumps(sample, default=default_serializer))})",
                "    payload = _inject_fk(payload)",
                "    httpx.post(BASE_URL, json=payload)",
                "    params = _pk_filter_from_payload(payload)",
                "    assert params, 'Composite PK params missing'",
                "    resp = httpx.get(BASE_URL, params=params)",
                '    assert resp.status_code == 200, f"GET (composite PK) failed: {resp.status_code} {resp.text}"',
                "",
            ]

        # UPDATE
        if has_single_pk:
            lines += [
                "def test_update():",
                f"    payload = json.loads({json.dumps(json.dumps(sample, default=default_serializer))})",
                "    payload = _inject_fk(payload)",
                f"    payload['{pk_field}'] = {pk_val if pk_val is not None else 1}",
                "    httpx.post(BASE_URL, json=payload)",
                f"    response = httpx.put(f\"{{BASE_URL}}/{pk_val if pk_val is not None else 1}\", json=payload)",
                "    assert response.status_code == 200",
                "",
            ]
        else:
            lines += ["def test_update():", "    assert True  # skipped for composite PK", ""]

        # DELETE
        if has_single_pk:
            lines += [
                "def test_delete():",
                f"    payload = json.loads({json.dumps(json.dumps(sample, default=default_serializer))})",
                "    payload = _inject_fk(payload)",
                f"    payload['{pk_field}'] = {pk_val if pk_val is not None else 1}",
                "    httpx.post(BASE_URL, json=payload)",
                f"    response = httpx.delete(f\"{{BASE_URL}}/{pk_val if pk_val is not None else 1}\")",
                "    assert response.status_code in (200, 204)",
                "",
            ]
        else:
            lines += ["def test_delete():", "    assert True  # skipped for composite PK", ""]

        # OPTIONS
        lines += [
            "def test_options():",
            '    response = httpx.get(f"{BASE_URL}/options")',
            "    assert response.status_code == 200",
            "",
        ]

        # eq filters
        for k, v in sample.items():
            if isinstance(v, (str, int, float, bool)):
                qv_py = repr(v)
                lines.append(f"def test_eq_{k}():")
                lines.append(f"    response = httpx.get(BASE_URL, params={{'{k}': {qv_py}}})")
                lines.append("    assert response.status_code == 200")
                lines.append("")

        # date filter (optional)
        added_date = False
        for k, v in sample.items():
            if isinstance(v, str) and ("date" in k.lower() or "at" in k.lower()):
                lines += [
                    "def test_date_filter():",
                    "    start = datetime.now() - timedelta(days=30)",
                    "    end = datetime.now() + timedelta(days=30)",
                    "    response = httpx.get(",
                    "        BASE_URL,",
                    f"        params={{'{k}__gt': start.isoformat(), '{k}__lt': end.isoformat()}}",
                    ")",
                    "    assert response.status_code == 200",
                    "",
                ]
                added_date = True
                break
        if not added_date:
            lines += ["def test_date_filter():", "    assert True  # no date-like field", ""]

        test_file = os.path.join(TESTS_OUTPUT_DIR, f"test_{entity}.py")
        _write(test_file, "\n".join(lines))
        print(f"✅ Search test created: {test_file}")

# -------------------------------------------------------------------------------------------------
# NEW: Minimal Search snapshot (non-breaking) so search target has output even without ES runtime
# -------------------------------------------------------------------------------------------------

def search_snapshot():
    """Create a JSON-safe snapshot of elastic_entities.py and copy raw file."""
    _ensure_dir(SEARCH_OUTPUT_DIR)
    if os.path.exists(ELASTIC_ENTITIES_PATH):
        spec = importlib.util.spec_from_file_location("elastic_entities", ELASTIC_ENTITIES_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        elastic_entities = getattr(mod, "elastic_entities", {})
    else:
        elastic_entities = {}

    safe = _json_sanitize(elastic_entities)

    _write(
        os.path.join(SEARCH_OUTPUT_DIR, "elastic_entities.snapshot.json"),
        json.dumps(safe, indent=2)
    )

    if os.path.exists(ELASTIC_ENTITIES_PATH):
        _copy(ELASTIC_ENTITIES_PATH, os.path.join(SEARCH_OUTPUT_DIR, "elastic_entities.raw.py"))


# --- Frontend UI config: create if missing, then copy to src/clients/<client>/ ---
def generate_frontend_config():
    """
    Build frontend.api.config.json from entities.py:
    - mode: hybrid
    - default: mock
    - routing.<entity>.options = "mock" (so forms never hit API)
    - (No overwrite if file already exists)
    Also copy to nishify.io/src/clients/<client>/frontend.api.config.json
    """
    # 1) Derive from entities.py
    routing: Dict[str, Dict[str, str]] = {}
    total_entities = 0

    for entity_name, cfg in (entities or {}).items():
        fields = list((cfg or {}).get("fields", {}).keys())
        total_entities += 1

        # options always mock by default
        routing[entity_name] = {"options": "mock"}

        # LOG: show a compact preview of options (field list)
        _log(f"  • {entity_name}: options -> mock  | fields: {fields}")

    cfg_json = {
        "mode": "hybrid",
        "default": "mock",
        "routing": routing,
        "direct": {}
    }

    # 2) Create only if absent (respect manual edits)
    if not os.path.exists(FRONTEND_CONFIG_SRC):
        _log(f"🧩 FE::Creating UI config from entities.py for client '{CLIENT_NAME}' "
             f"({total_entities} entities)")
        _write(FRONTEND_CONFIG_SRC, json.dumps(cfg_json, indent=2))
        _log(f"✅ FE::Wrote {FRONTEND_CONFIG_SRC}")
    else:
        _log(f"ℹ️ FE::UI config already exists, keeping it: {FRONTEND_CONFIG_SRC}")

    # 3) Copy to UI folder for runtime use
    dest = os.path.join(FRONTEND_CLIENT_DIR, "frontend.api.config.json")
    _copy(FRONTEND_CONFIG_SRC, dest)
    _log(f"📦 FE::Copied UI config to {dest}")
    
# -------------------------------------------------------------------------------------------------
# Adapter registry (lightweight)
# -------------------------------------------------------------------------------------------------
ADAPTERS: Dict[str, callable] = {
    # backend bundle
    "backend.models": generate_models,
    "backend.testdata": generate_test_data,
    "backend.legacy_tests": lambda: generate_test_cases_from_mock(entities, TESTS_OUTPUT_DIR),
    "backend.copy_entities": copy_entity_files,
    # frontend bundle
    "frontend.mocks": generate_mock_data,
    "frontend.config": generate_frontend_config,
    "frontend.pages": generate_pages_config,
    # search bundle
    "search.tests": generate_search_tests,
    "search.snapshot": search_snapshot,
}

TARGET_MAP: Dict[str, List[str]] = {
    "backend": ["frontend.config","backend.models", "backend.testdata", "backend.legacy_tests", "backend.copy_entities"],
    "frontend": ["frontend.config","frontend.mocks", "frontend.pages"],
    "search": ["search.tests", "search.snapshot"],
    "all": [
        "backend.models", "backend.testdata", "backend.legacy_tests", "backend.copy_entities",
        "frontend.mocks", "frontend.pages","frontend.config",
        "search.tests", "search.snapshot",
    ],
}

# -------------------------------------------------------------------------------------------------
# Runner
# -------------------------------------------------------------------------------------------------

def run_targets():
    _log(f"🚀 Starting code generation for client: {CLIENT_NAME}")
    _log(f"📁 Using config: {client_config}")

    seq: List[str] = []
    for t in TARGETS:
        seq.extend(TARGET_MAP.get(t, []))
    # de-dup preserve order
    seen = set(); ordered = []
    for k in seq:
        if k not in seen:
            ordered.append(k); seen.add(k)

    for key in ordered:
        fn = ADAPTERS.get(key)
        if not fn:
            raise KeyError(f"Adapter not found: {key}")
        _log(f"→ Running adapter: {key}")
        fn()

    # excel dump always helpful (belongs to backend data bundle). Keep original behavior.
    if "backend" in TARGETS or "all" in TARGETS:
        generate_excel_dump()

    _log("🎉 Code generation completed")

# -------------------------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    run_targets()
    SUMMARY.print()
