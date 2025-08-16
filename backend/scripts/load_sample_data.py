# backend/scripts/load_sample_data.py
import os, sys, importlib.util
from pathlib import Path
from sqlalchemy import Integer, select, func
from sqlalchemy.exc import SQLAlchemyError
from backend.utils.db import SessionLocal
from backend.utils.model_loader import get_model_class, get_all_models

# repo root on path
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

# env-only client
CLIENT = os.environ.get("CLIENT_NAME")
if not CLIENT:
    raise SystemExit("Set CLIENT_NAME, e.g. CLIENT_NAME=pioneer_wholesale_inc")

# load clients/<CLIENT>/entities.data.py
ENTITIES_DATA_PATH = ROOT / "clients" / CLIENT / "entities.data.py"
if not ENTITIES_DATA_PATH.exists():
    raise SystemExit(f"Not found: {ENTITIES_DATA_PATH}")

spec = importlib.util.spec_from_file_location("entities_data", str(ENTITIES_DATA_PATH))
entities_data_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entities_data_module)

# support both names exported by data_faker
DATA = getattr(entities_data_module, "sample_data", None) or getattr(entities_data_module, "entities_data", None)
if DATA is None:
    raise SystemExit("entities.data.py must export `sample_data` or `entities_data`.")

def _rows_for(entity_info):
    # old shape: {"sample_data": [...]}
    if isinstance(entity_info, dict) and "sample_data" in entity_info:
        return entity_info["sample_data"] or []
    # new shape: list of rows
    if isinstance(entity_info, list):
        return entity_info
    return []

def _ensure_id_if_needed(db, model, rows):
    """
    If table has an 'id' column and rows don't include it, synthesize IDs when
    it's required (PK or non-null without defaults). Works for int/string.
    """
    id_col = model.__table__.columns.get("id")
    # NEVER truth-test a Column; compare to None explicitly
    if id_col is None or any("id" in r for r in rows):
        return rows

    need = bool(getattr(id_col, "primary_key", False)) or (
        getattr(id_col, "nullable", True) is False
        and getattr(id_col, "default", None) is None
        and getattr(id_col, "server_default", None) is None
    )
    if not need:
        return rows

    start = 1
    if isinstance(id_col.type, Integer):
        try:
            max_id = db.execute(select(func.max(getattr(model, "id")))).scalar()
            if max_id is not None:
                start = int(max_id) + 1
        except Exception:
            pass

    out = []
    for idx, r in enumerate(rows, start=start):
        rr = dict(r)
        rr["id"] = idx if isinstance(id_col.type, Integer) else f"{model.__tablename__}_{idx}"
        out.append(rr)
    return out

def main():
    # ✅ import ALL models up front so string relationships like "Salesperson"/"State" resolve
    get_all_models(CLIENT)

    db = SessionLocal()
    try:
        for entity_name, entity_info in DATA.items():
            rows = _rows_for(entity_info)
            if not rows:
                print(f"⚠️  No rows for: {entity_name}")
                continue

            try:
                model = get_model_class(CLIENT, entity_name)

                # ensure id present when required
                rows = _ensure_id_if_needed(db, model, rows)

                # clear + ORM bulk insert (safe)
                db.query(model).delete(synchronize_session=False)
                db.bulk_insert_mappings(model, rows, render_nulls=True)
                db.commit()
                print(f"✅ Inserted {len(rows)} rows into '{entity_name}'")
            except SQLAlchemyError as e:
                db.rollback()
                print(f"❌ Error inserting into '{entity_name}': {e}")
            except Exception as e:
                db.rollback()
                print(f"❌ Error inserting into '{entity_name}': {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
