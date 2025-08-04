import os
import importlib.util
from sqlalchemy import insert, delete
from backend.utils.db import SessionLocal
from backend.utils.model_loader import get_model_class
from backend.utils.config import get_client_name

# 🧠 Get client and file path
client_name = get_client_name()
CLIENT_DIR = os.path.join("clients", client_name)
ENTITIES_DATA_PATH = os.path.join(CLIENT_DIR, "entities.data.py")

# 📦 Load entities.data.py dynamically
spec = importlib.util.spec_from_file_location("entities_data", ENTITIES_DATA_PATH)
entities_data_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entities_data_module)
entities_data = entities_data_module.entities_data

# 🔌 DB session
db = SessionLocal()

# 🛠 Load + Insert for each entity
for entity_name, entity_info in entities_data.items():
    rows = entity_info.get("sample_data", [])
    if not rows:
        print(f"⚠️  No sample_data for: {entity_name}")
        continue

    try:
        model = get_model_class(client_name, entity_name)
        db.execute(delete(model))  # ✅ Clear old records
        db.execute(insert(model).values(rows))  # ✅ Insert fresh rows
        db.commit()
        print(f"✅ Inserted {len(rows)} rows into '{entity_name}'")
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting into '{entity_name}': {e}")

db.close()
