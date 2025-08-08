from elasticsearch import Elasticsearch
from backend.utils.model_loader import get_model_class
from backend.utils.config import get_client_name
from backend.utils.db import SessionLocal
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import importlib.util
import os
import sys

# -------------------------
# Elastic client (ES 8 compat via v9 client)
# -------------------------

# ---- Elasticsearch client (v9 client talking to ES 8 via compat headers) ----
import os, sys
from urllib.parse import urlparse
from elasticsearch import Elasticsearch
from elastic_transport import Transport, NodeConfig

ES_URL = os.getenv("ES_URL", "http://localhost:9200")
ES_USER = os.getenv("ES_USER")
ES_PASS = os.getenv("ES_PASS")
ES_API_KEY = os.getenv("ES_API_KEY")

# ES 8 needs these headers when using v9 client
COMPAT_HEADERS = {
    "Accept": "application/vnd.elasticsearch+json; compatible-with=8",
    "Content-Type": "application/vnd.elasticsearch+json; compatible-with=8",
}

# --- Elasticsearch client (v9 client + ES 9) ---
import os, sys
from elasticsearch import Elasticsearch

ES_URL = os.getenv("ES_URL", "http://localhost:9200")
ES_USER = os.getenv("ES_USER")
ES_PASS = os.getenv("ES_PASS")
ES_API_KEY = os.getenv("ES_API_KEY")

auth_kwargs = {}
if ES_API_KEY:
    auth_kwargs["api_key"] = ES_API_KEY
elif ES_USER and ES_PASS:
    auth_kwargs["basic_auth"] = (ES_USER, ES_PASS)

es = Elasticsearch(ES_URL, **auth_kwargs)

# sanity check
try:
    info = es.info()
    print(f"✅ Connected to Elasticsearch {info['version']['number']} at {ES_URL}")
except Exception as e:
    print(f"❌ Could not connect to Elasticsearch at {ES_URL}: {e}")
    sys.exit(1)
# --- end client setup ---


client_name = get_client_name()
client_dir = os.path.join(os.path.dirname(__file__), "..", "clients", client_name)
elastic_config_path = os.path.join(client_dir, "elastic_entities.py")
spec = importlib.util.spec_from_file_location("elastic_entities", elastic_config_path)
elastic_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(elastic_module)
elastic_entities = elastic_module.elastic_entities

# -------------------------
# DB session
# -------------------------

db = SessionLocal()

def get_entity_data(entity_name, config):
    model = get_model_class(client_name, entity_name)
    query = select(model)

    if "follow_fk" in config:
        fk_fields = config["follow_fk"].keys() if isinstance(config["follow_fk"], dict) else config["follow_fk"]
        for fk_field in fk_fields:
            query = query.options(joinedload(getattr(model, fk_field)))

    return db.scalars(query).all()

def serialize_row(row, config, prefix="", flatten=True):
    result = {}
    fields = [c.name for c in row.__table__.columns] if config.get("__all__") else config.get("fields", [])

    for field in fields:
        value = getattr(row, field, None)
        key = f"{prefix}.{field}" if prefix and flatten else field
        result[key.replace(".", "_") if flatten else key] = value

    if "follow_fk" in config:
        if isinstance(config["follow_fk"], dict):
            fk_items = config["follow_fk"].items()
        else:
            fk_items = ((name, config) for name in config["follow_fk"])

        for fk_field, fk_conf in fk_items:
            related = getattr(row, fk_field, None)
            if related:
                nested = serialize_row(
                    related,
                    fk_conf,
                    f"{prefix}.{fk_field}" if prefix else fk_field,
                    flatten=flatten
                )
                result.update(nested if flatten else {fk_field: nested})

    # Aliases
    for orig, alias in config.get("field_aliases", {}).items():
        if orig in result:
            result[alias] = result.pop(orig)

    return result

def index_entity_data(entity_name):
    if entity_name not in elastic_entities:
        print(f"⚠️  No elastic config found for entity: {entity_name}")
        return

    config = elastic_entities[entity_name]
    model = get_model_class(client_name, entity_name)
    index_name = config.get("index_name", entity_name)
    flatten = config.get("flatten", True)

    print(f"🔍 Indexing: {entity_name} → {index_name}")

    data = get_entity_data(entity_name, config)
    count = 0

    for row in data:
        doc = serialize_row(row, config, flatten=flatten)

        if config.get("exclude_if") and config["exclude_if"](doc):
            continue

        doc_id = doc.get("id")
        if not doc_id:
            continue

        es.index(index=index_name, id=doc_id, document=doc)
        count += 1

    print(f"✅ Indexed {count} documents to `{index_name}`")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("ℹ️  Indexing ALL entities...")
        for entity in elastic_entities:
            index_entity_data(entity)
    else:
        for entity in args:
            index_entity_data(entity)

    db.close()
