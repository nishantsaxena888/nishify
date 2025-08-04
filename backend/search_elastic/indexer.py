from elasticsearch import Elasticsearch
from backend.utils.model_loader import get_model_class
from backend.utils.config import get_client_name
from backend.utils.db import SessionLocal
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import importlib.util
import os

# 🔁 Load config dynamically
client_name = get_client_name()
client_dir = os.path.join(os.path.dirname(__file__), "..", "clients", client_name)
elastic_config_path = os.path.join(client_dir, "elastic_entities.py")
spec = importlib.util.spec_from_file_location("elastic_entities", elastic_config_path)
elastic_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(elastic_module)
elastic_entities = elastic_module.elastic_entities

# 🔌 Elastic & DB
es = Elasticsearch("http://localhost:9200")
db = SessionLocal()


def get_entity_data(entity_name, config):
    model = get_model_class(client_name, entity_name)
    query = select(model)

    if "follow_fk" in config:
        for fk_field in config["follow_fk"]:
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
        for fk_field, fk_conf in config["follow_fk"].items():
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
    import sys

    args = sys.argv[1:]
    if not args:
        print("ℹ️  Indexing ALL entities...")
        for entity in elastic_entities:
            index_entity_data(entity)
    else:
        for entity in args:
            index_entity_data(entity)

    db.close()
