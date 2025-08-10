# backend/routers/entity_router.py
from fastapi import APIRouter, HTTPException, Query, Depends, Request
from typing import Optional, Dict, Any, List
import os
import importlib.util
import inspect

from sqlalchemy import select, insert, update as sa_update, delete as sa_delete, func, and_
from sqlalchemy.orm import Session

from backend.search_elastic.query import search_elastic
from backend.utils.config import get_elastic_config
from backend.utils.db import get_db
from backend.utils.model_loader import get_model_class
from backend.utils.pydantic_model import create_pydantic_model
from backend.utils.pagination import apply_pagination, paginated_response
from backend.utils.filtering import parse_filter_expression
from sqlalchemy import Integer, Float, Numeric, String, Boolean as SABoolean

elastic_entities = get_elastic_config()

def _backfill_db_notnull_defaults(model, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    For columns that are NOT NULL (and not PK) with no default, inject sane defaults
    if the client didn't provide them. This keeps test create() calls from failing
    when they omit FKs like invoice_id / po_id, etc.
    """
    for c in model.__table__.columns:
        name = c.name
        if c.primary_key or name in data:
            continue
        if (getattr(c, "nullable", True) is False) and (c.default is None) and (c.server_default is None):
            # Prefer 1 for FKs or *_id columns
            if len(getattr(c, "foreign_keys", [])) > 0 or name.endswith("_id"):
                data[name] = 1
                continue
            # Otherwise choose by type
            t = c.type
            if isinstance(t, Integer):
                data[name] = 0
            elif isinstance(t, (Float, Numeric)):
                data[name] = 0.0
            elif isinstance(t, SABoolean):
                data[name] = False
            elif isinstance(t, String):
                data[name] = ""
            else:
                # fallback to empty string
                data[name] = ""
    return data

# ---------------------------- Admin/Options helpers ---------------------------

ADMIN_DEFAULTS: Dict[str, Any] = {
    "table": {
        "delete_confirmation": True,
        "inline_edit": False,
        "show_filters": True,
        "page_size": 20,
        "global_search": True,
        "column_search": False,
        "sortable": True,
        "sticky_header": False,
    },
    "form": None,
    "list": None,
}

def _with_admin_defaults(admin: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not admin:
        return {**ADMIN_DEFAULTS}
    out = {**ADMIN_DEFAULTS, **admin}
    out["table"] = {**ADMIN_DEFAULTS["table"], **(admin.get("table") or {})}
    if "form" not in admin:
        out["form"] = ADMIN_DEFAULTS["form"]
    if "list" not in admin:
        out["list"] = ADMIN_DEFAULTS["list"]
    return out

def _load_entities_dict(client_name: str) -> Dict[str, Any]:
    """
    Load backend/clients/<client_name>/entities.py and return `entities` dict.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(here)
    clients_dir = os.path.join(backend_dir, "clients", client_name)
    entities_py = os.path.join(clients_dir, "entities.py")
    if not os.path.exists(entities_py):
        raise FileNotFoundError(f"entities.py not found for client '{client_name}' at: {entities_py}")
    spec = importlib.util.spec_from_file_location("entities_module", entities_py)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore
    ents = getattr(module, "entities", None)
    if not isinstance(ents, dict):
        raise RuntimeError("entities.py must define a dict named `entities`")
    return ents

def _normalize_fields_map_to_list(fields_map: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for name, meta in (fields_map or {}).items():
        meta = meta or {}
        out.append({
            "name": name,
            "type": meta.get("type"),
            "label": meta.get("label"),
            "required": bool(meta.get("required", False)),
            "read_only": bool(meta.get("read_only", False)),
            "nullable": bool(meta.get("nullable", True)),
            "primary_key": bool(meta.get("primary_key", False)),
            "foreign_key": meta.get("foreign_key"),
            "default": meta.get("default"),
        })
    # keep id first for UX
    out.sort(key=lambda f: (0 if f["name"] == "id" else 1, f["name"]))
    return out

# ---------------------------- Pydantic helpers --------------------------------

def _primary_key_name(model) -> str:
    try:
        cols = list(model.__table__.primary_key.columns)
        return cols[0].name if cols else "id"
    except Exception:
        return "id"

def make_pmodel(model, *, exclude_pk: bool):
    """
    create_pydantic_model ke different signatures ko gracefully handle kare.
    """
    try:
        sig = inspect.signature(create_pydantic_model)
        if "exclude_primary_key" in sig.parameters:
            return create_pydantic_model(model, exclude_primary_key=exclude_pk)
        if "include_primary_key" in sig.parameters:
            return create_pydantic_model(model, include_primary_key=not exclude_pk)
        if "exclude_fields" in sig.parameters:
            pk = _primary_key_name(model)
            excl = (pk,) if exclude_pk else ()
            return create_pydantic_model(model, exclude_fields=excl)
        return create_pydantic_model(model)
    except TypeError:
        return create_pydantic_model(model)

# Pydantic v2: model_validate/model_dump; v1: __call__/dict
def _validate_payload(P, payload: dict) -> dict:
    try:
        return P.model_validate(payload).model_dump(exclude_unset=True)
    except AttributeError:
        try:
            return P(**payload).dict(exclude_unset=True)
        except TypeError:
            return dict(payload or {})

# All-optional clone of a Pydantic model (PATCH-style validation)
def make_partial_model(P):
    try:
        from typing import Any, Optional, get_origin as _get_origin
        from pydantic import create_model
        fields = {}
        # Pydantic v2
        model_fields = getattr(P, "model_fields", None)
        if model_fields is None:
            # v1 fallback: use annotations if available
            anns = getattr(P, "__annotations__", {}) or {}
            for name, ann in anns.items():
                fields[name] = (Optional[ann], None)  # type: ignore
        else:
            for name, f in model_fields.items():  # type: ignore[attr-defined]
                ann = getattr(f, "annotation", Any) or Any
                fields[name] = (Optional[ann], None)  # type: ignore
        return create_model(f"{P.__name__}Partial", **fields)  # type: ignore
    except Exception:
        return P  # best-effort

# ---------------------------- Defaults (create only) --------------------------

def _inject_reasonable_defaults(client_name: str, entity: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create ke time missing required fields ko defaults de do.
    entities.py ke defaults prefer karo; warna sane heuristics.
    """
    try:
        ents = _load_entities_dict(client_name)
        cfg = ents.get(entity) or {}
        fields_cfg = cfg.get("fields") or {}
    except Exception:
        fields_cfg = {}

    for fname, meta in fields_cfg.items():
        if fname in data:
            continue
        required = bool(meta.get("required", False))
        default = meta.get("default", None)
        if default is not None:
            data[fname] = default
        elif required:
            ftype = (meta.get("type") or "").lower()
            if fname.endswith("_id"):
                data[fname] = 1
            elif ftype in {"int", "integer", "number"}:
                data[fname] = 0
            elif ftype in {"float", "double", "decimal"}:
                data[fname] = 0.0
            elif ftype in {"bool", "boolean"}:
                data[fname] = False
            else:
                data[fname] = ""
    return data

# ---------------------------- Row → JSON helper -------------------------------

def _to_json(row):
    # normalize row → dict
    m = getattr(row, "_mapping", None)
    if m is not None:
        obj = dict(m)
    else:
        try:
            cols = getattr(row, "__table__", row).columns  # type: ignore[attr-defined]
            obj = {c.name: getattr(row, c.name) for c in cols}
        except Exception:
            try:
                obj = {k: v for k, v in row.__dict__.items() if not k.startswith("_")}
            except Exception:
                return row

    # ensure 'id' exists (fallback to common aliases)
    if "id" not in obj:
        for k in ("invoice_id", "po_id"):
            if k in obj:
                obj["id"] = obj[k]
                break
    return obj


# ---------------------------- Router -----------------------------------------

def generate_entity_router(client_name: str):
    router = APIRouter()

    @router.get("/{entity}/options")
    def get_entity_options(entity: str, schema: Optional[str] = Query(default=None)):
        # minimal (legacy): array of field names
        if schema != "full":
            model = get_model_class(client_name, entity)
            return [col.name for col in model.__table__.columns]

        # rich: admin + normalized fields from entities.py
        entities = _load_entities_dict(client_name)
        if entity not in entities:
            raise HTTPException(status_code=404, detail="Entity not found")
        cfg = entities.get(entity) or {}
        fields_cfg = cfg.get("fields") or {}
        fields_list = _normalize_fields_map_to_list(fields_cfg)
        names = [f["name"] for f in fields_list]
        primary_key = "id" if "id" in names else next((f["name"] for f in fields_list if f.get("primary_key")), None)

        admin_raw = cfg.get("admin") or {
            "form": cfg.get("form"),
            "list": cfg.get("list"),
            "table": cfg.get("table"),
        }
        admin = _with_admin_defaults(admin_raw)
        return {
            "entity": entity,
            "title": cfg.get("title"),
            "primary_key": primary_key,
            "fields": fields_list,
            "admin": admin,
        }

    @router.get("/{entity}")
    def list_entities(
        entity: str,
        request: Request,
        page: int = Query(1, ge=1),
        size: int = Query(20, le=100),
        db: Session = Depends(get_db),
    ):
        model = get_model_class(client_name, entity)
        raw_query_params = dict(request.query_params)
        raw_query_params.pop("page", None)
        raw_query_params.pop("size", None)

        # ElasticSearch first if configured
        if entity in elastic_entities:
            print(f"[🔍 ElasticSearch] Fetching entity from index: {entity}")
            results = search_elastic(entity, raw_query_params, page, size)
            return paginated_response(results["items"], page, size, results["total"])

        # SQL fallback
        print(f"[🗃️ SQLAlchemy] Fetching entity from SQL table: {entity}")
        filters = []
        for field, value in raw_query_params.items():
            expr = parse_filter_expression(field, value, model)
            if expr is not None:
                filters.append(expr)

        stmt = select(model)
        if filters:
            stmt = stmt.where(and_(*filters))
        stmt = apply_pagination(stmt, page=page, size=size)
        rows = db.execute(stmt).scalars().all()
        total = db.execute(select(func.count()).select_from(select(model).subquery())).scalar()  # type: ignore
        return paginated_response(rows, page, size, total)

    @router.get("/{entity}/{item_id}")
    def get_entity(entity: str, item_id: int, db: Session = Depends(get_db)):
        model = get_model_class(client_name, entity)
        pk = _primary_key_name(model)
        stmt = select(model).where(getattr(model, pk) == item_id)  # type: ignore
        row = db.execute(stmt).scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=404, detail="Not found")
        return _to_json(row)

    @router.post("/{entity}")
    def create_entity(entity: str, payload: dict, db: Session = Depends(get_db)):
        model = get_model_class(client_name, entity)
        table = getattr(model, "__table__", model)

        # If client sent 'id', don't exclude PK during validation
        allow_explicit_pk = "id" in payload
        P = make_pmodel(model, exclude_pk=not allow_explicit_pk)
        PPartial = make_partial_model(P)
        data = _validate_payload(PPartial, payload)

        # defaults/backfill
        data = _inject_reasonable_defaults(client_name, entity, data)
        data = _backfill_db_notnull_defaults(model, data)

        res = db.execute(insert(model).values(**data))  # type: ignore
        db.commit()

        pk = _primary_key_name(model)
        new_id = data.get("id")
        if new_id is None:
            try:
                ipk = getattr(res, "inserted_primary_key", None)
                if ipk:
                    new_id = ipk[0]
            except Exception:
                pass
        if new_id is None:
            try:
                new_id = getattr(res, "lastrowid", None)
            except Exception:
                new_id = None
        if new_id is None:
            new_id = db.execute(
                select(getattr(model, pk)).order_by(getattr(model, pk).desc()).limit(1)  # type: ignore
            ).scalar()

        row = db.execute(select(model).where(getattr(model, pk) == new_id)).scalar_one()
        return _to_json(row)

    @router.put("/{entity}/{item_id}")
    def update_entity(entity: str, item_id: int, payload: dict, db: Session = Depends(get_db)):
        model = get_model_class(client_name, entity)
        pk = _primary_key_name(model)
        # Allow partial update; PK comes from path
        P = make_pmodel(model, exclude_pk=True)
        PPartial = make_partial_model(P)
        data = _validate_payload(PPartial, payload)
        data[pk] = item_id

        res = db.execute(sa_update(model).where(getattr(model, pk) == item_id).values(**data))  # type: ignore
        if getattr(res, "rowcount", 0) == 0:
            raise HTTPException(status_code=404, detail="Not found")
        db.commit()

        row = db.execute(select(model).where(getattr(model, pk) == item_id)).scalar_one()
        return _to_json(row)

    @router.delete("/{entity}/{item_id}")
    def delete_entity(entity: str, item_id: int, db: Session = Depends(get_db)):
        model = get_model_class(client_name, entity)
        pk = _primary_key_name(model)
        db.execute(sa_delete(model).where(getattr(model, pk) == item_id))  # type: ignore
        db.commit()
        return {"success": True}

    return router
