import os, sys
from pathlib import Path
from sqlalchemy import select, func
from backend.utils.db import SessionLocal
from backend.utils.model_loader import get_all_models

# repo root on path
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

# env-only client
CLIENT = os.environ.get("CLIENT_NAME")
if not CLIENT:
    raise SystemExit("Set CLIENT_NAME, e.g. CLIENT_NAME=pioneer_wholesale_inc")

# load models for this client
models = get_all_models(CLIENT)
if not models:
    raise SystemExit(f"No models found for client={CLIENT}. Did you generate models and have models/__init__.py?")

# count rows per table
db = SessionLocal()
try:
    total = 0
    for M in sorted(models, key=lambda m: m.__tablename__):
        n = db.execute(select(func.count()).select_from(M)).scalar_one()
        print(f"{M.__tablename__}: {n}")
        total += int(n)
    print(f"TOTAL: {total}")
finally:
    db.close()
