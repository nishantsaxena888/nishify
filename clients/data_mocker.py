import os
import sys
import random
import json
import importlib.util

def get_client_paths():
    if len(sys.argv) < 2:
        raise ValueError("Client name must be passed as an argument. Usage: python script.py <client_name>")

    client_name = sys.argv[-1]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))
    client_dir = os.path.join(root_dir, "clients", client_name)
    entities_path = os.path.join(client_dir, "entities.py")
    output_path = os.path.join(client_dir, "entities.data.py")

    return client_name, script_dir, root_dir, client_dir, entities_path, output_path

def load_entities(entities_path):
    spec = importlib.util.spec_from_file_location("entities", entities_path)
    entities = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(entities)
    return entities.entities

def generate_sample_value(field_type):
    if field_type == "int":
        return random.randint(1, 1000)
    elif field_type == "float":
        return round(random.uniform(10.0, 999.9), 2)
    elif field_type == "bool":
        return random.choice([True, False])
    elif field_type == "datetime":
        return "2023-01-01T00:00:00"
    return f"Sample {field_type.capitalize()}"

def generate_sample_data(entities):
    for entity_name, config in entities.items():
        if "sample_data" not in config or not config["sample_data"]:
            sample = {}
            for field, fconfig in config["fields"].items():
                sample[field] = generate_sample_value(fconfig["type"])
            config["sample_data"] = [sample]
    return entities

def write_entities_data_py(entities, output_path):
    with open(output_path, "w") as f:
        f.write("entities = ")
        json.dump(entities, f, indent=4)

def main():
    client_name, script_dir, root_dir, client_dir, entities_path, output_path = get_client_paths()
    entities = load_entities(entities_path)
    enriched = generate_sample_data(entities)
    write_entities_data_py(enriched, output_path)
    print(f"✅ Generated sample data at {output_path}")

if __name__ == "__main__":
    main()
