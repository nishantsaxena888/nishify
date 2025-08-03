# data_faker.py
import os
import sys
import random
import importlib.util
from faker import Faker
import json

faker = Faker()

if len(sys.argv) < 2:
    raise ValueError("Usage: python data_faker.py <client_name>")

CLIENT_NAME = sys.argv[1]
INFRA_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(INFRA_DIR, ".."))
CLIENT_DIR = os.path.join(ROOT_DIR, "clients", CLIENT_NAME)
ENTITIES_PATH = os.path.join(CLIENT_DIR, "entities.py")
ENTITIES_DATA_PATH = os.path.join(CLIENT_DIR, "entities.data.py")

# Load entities.py
spec = importlib.util.spec_from_file_location("entities", ENTITIES_PATH)
entities = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entities)
entities_config = entities.entities

def generate_faker_value(faker_string):
    try:
        return eval(f"faker.{faker_string}")
    except Exception as e:
        print(f"⚠️ Invalid faker expression '{faker_string}': {e}")
        return None

def generate_default_value(field_type):
    if field_type == "int":
        return random.randint(1, 9999)
    elif field_type == "float":
        return round(random.uniform(1, 9999), 2)
    elif field_type == "str":
        return faker.word()
    elif field_type == "bool":
        return random.choice([True, False])
    elif field_type == "date":
        return str(faker.date_this_year())
    return None

entities_data = {}
for entity_name, config in entities_config.items():
    fields = config.get("fields", {})
    rows = []
    for _ in range(5):
        row = {}
        for field_name, field_config in fields.items():
            if "faker" in field_config:
                value = generate_faker_value(field_config["faker"])
            else:
                value = generate_default_value(field_config.get("type"))
            row[field_name] = value
        rows.append(row)
    entities_data[entity_name] = {"sample_data": rows}


with open(ENTITIES_DATA_PATH, "w") as f:
    f.write("entities_data = ")
    json.dump(entities_data, f, indent=2)

print(f"✅ Created: {ENTITIES_DATA_PATH}")
