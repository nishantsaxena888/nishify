import os
import sys
from sqlalchemy import select, func
from backend.utils.db import SessionLocal
from backend.utils.model_loader import get_model_class
from backend.utils.config import get_client_name
import importlib.util

client_name = get_client_name()
db = SessionLocal()

# 🔍 Load all entity names from entities.data.py if no arguments passed
if len(sys.argv) > 1:
    entities = sys.argv[1:]
else:
    CLIENT_DIR = os.path.join("clients", client_name)
    ENTITIES_DATA_PATH = os.path.join(CLIENT_DIR, "entities.data.py")
    
    spec = importlib.util.spec_from_file_location("entities_data", ENTITIES_DATA_PATH)
    entities_data_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(entities_data_module)
    entities_data = entities_data_module.entities_data
    entities = list(entities_data.keys())

print(f"🔍 Showing row counts for {len(entities)} entities...\n")

for entity_name in entities:
    try:
        model = get_model_class(client_name, entity_name)
        count = db.scalar(select(func.count()).select_from(model))
        print(f"{entity_name}: {count} rows")
    except Exception as e:
        print(f"❌ Failed to load {entity_name}: {e}")

db.close()
