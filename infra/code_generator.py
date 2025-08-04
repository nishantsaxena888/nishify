import os
import importlib.util
from datetime import datetime, date
import json
import pandas as pd
import sys
import shutil
import pprint

LOG = True

if len(sys.argv) < 2:
    raise ValueError("Usage: python code_generator.py <client_name> [mock]")

CLIENT_NAME = sys.argv[1]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))  # nishify root
CLIENTS_DIR = os.path.join(ROOT_DIR, "clients")
CLIENT_DIR = os.path.join(CLIENTS_DIR, CLIENT_NAME)
ENTITIES_PATH = os.path.join(CLIENT_DIR, "entities.py")
CONFIG_PATH = os.path.join(CLIENT_DIR, "config.json")
PAGES_OUTPUT_DIR = os.path.join(ROOT_DIR, f"nishify.io/src/clients/{CLIENT_NAME}")
TESTS_OUTPUT_DIR = os.path.join(ROOT_DIR, f"backend/tests/{CLIENT_NAME}")
MODEL_OUTPUT_DIR = os.path.join(ROOT_DIR, f"backend/clients/{CLIENT_NAME}/models")
MOCK_OUTPUT_DIR = os.path.join(ROOT_DIR, f"nishify.io/src/lib/api/mock/{CLIENT_NAME}")
TESTDATA_OUTPUT_DIR = os.path.join(ROOT_DIR, f"backend/clients/{CLIENT_NAME}/test_data")
EXCEL_OUTPUT_FILE = os.path.join(TESTDATA_OUTPUT_DIR, "test_data.xlsx")

if not os.path.exists(ENTITIES_PATH):
    print(f"❌ Client '{CLIENT_NAME}' not found at {ENTITIES_PATH}\n")
    print("📁 Available clients:")
    for folder in os.listdir(CLIENTS_DIR):
        if os.path.isdir(os.path.join(CLIENTS_DIR, folder)):
            print(f"- {folder}")

    scaffold = input(f"\nWould you like to scaffold a new client '{CLIENT_NAME}'? (y/n): ").strip().lower()
    if scaffold == 'y':
        os.makedirs(CLIENT_DIR, exist_ok=True)
        with open(ENTITIES_PATH, 'w') as f:
            f.write("entities = {}\n")
        ENTITIES_DATA_PATH = os.path.join(CLIENT_DIR, "entities.data.py")
        with open(ENTITIES_DATA_PATH, 'w') as f:
            f.write("entities_data = {}\n")
        with open(CONFIG_PATH, 'w') as f:
            json.dump({
                "env": {
                    "dev_url": "http://localhost:8000/api",
                    "prod_url": "https://api.example.com"
                },
                "use_mock": True,
                "theme": "default",
                "auth_mode": "none"
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

spec_entities = importlib.util.spec_from_file_location("entities", ENTITIES_PATH)
entities_module = importlib.util.module_from_spec(spec_entities)
spec_entities.loader.exec_module(entities_module)
entities = entities_module.entities

ENTITIES_DATA_PATH = os.path.join(CLIENT_DIR, "entities.data.py")
if os.path.exists(ENTITIES_DATA_PATH):
    spec_data = importlib.util.spec_from_file_location("entities_data", ENTITIES_DATA_PATH)
    data_module = importlib.util.module_from_spec(spec_data)
    spec_data.loader.exec_module(data_module)
    data_entities = data_module.entities_data

    for key, value in data_entities.items():
        if key in entities:
            entities[key]["sample_data"] = value.get("sample_data", [])
        else:
            print(f"⚠️ {key} found in entities.data.py but not in entities.py — skipping.")
else:
    print("⚠️ entities.data.py not found — proceeding without sample data.")

def log(msg):
    if LOG:
        print(msg)

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
        "datetime": "DateTime",
    }.get(field_type, "String")

def generate_models():
    os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)

    for entity, config in entities.items():
        fields = config["fields"]

        has_primary_key = any(field_conf.get("primary_key") for field_conf in fields.values())
        if not has_primary_key:
            log(f"⚠️ Skipping model for {entity} (no primary key found)")
            continue

        lines = [
            "from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey",
            "from sqlalchemy.orm import relationship",
            "from datetime import datetime",
            "\nfrom backend.utils.db_base import Base",
            f"\nclass {entity.capitalize()}(Base):",
            f"    __tablename__ = '{entity}'",
        ]

        for field_name, field_conf in fields.items():
            sql_type = type_map(field_conf["type"])
            opts = []
            args = [sql_type]
            if field_conf.get("foreign_key"):
                args.append(f"ForeignKey('{field_conf['foreign_key']}.id')")

            kwargs = []
            if field_conf.get("primary_key"):
                kwargs.append("primary_key=True")
            if field_conf.get("required"):
                kwargs.append("nullable=False")
            if field_conf.get("auto_now"):
                kwargs.append("default=datetime.utcnow")

            all_args = args + kwargs
            line = f"    {field_name} = Column({', '.join(all_args)})"
            lines.append(line)

            if field_conf.get("foreign_key"):
                fk_entity = field_conf["foreign_key"].split(".")[0]
                rel_name = fk_entity  # Always use this
                rel_class = fk_entity.capitalize()
                lines.append(f"    {rel_name} = relationship(\"{rel_class}\")")



        model_code = "\n".join(lines)
        model_path = os.path.join(MODEL_OUTPUT_DIR, f"{entity}.py")
        with open(model_path, "w") as f:
            f.write(model_code)
        log(f"✅ Generated model for {entity} at {model_path}")

def generate_mock_data():
    os.makedirs(MOCK_OUTPUT_DIR, exist_ok=True)

    for entity, config in entities.items():
        sample_data = config.get("sample_data", [])
        handlers = {
            "options": f"() => {str([k for k in config['fields'].keys()])}",
            "get": f"() => {sample_data}",
            "getOne": f"(id) => {sample_data}[0]",
            "post": "(payload) => ({ ...payload, id: Math.floor(Math.random() * 10000) })",
            "update": "(payload) => payload"
        }

        lines = [f"export const {entity} = {{"] + [f"  {k}: {v}," for k, v in handlers.items()] + ["};"]

        mock_path = os.path.join(MOCK_OUTPUT_DIR, f"{entity}.ts")
        with open(mock_path, "w") as f:
            f.write("\n".join(lines))
        log(f"✅ Generated mock for {entity} at {mock_path}")

def generate_test_data():
    os.makedirs(TESTDATA_OUTPUT_DIR, exist_ok=True)

    for entity, config in entities.items():
        data = config.get("sample_data", [])
        json_path = os.path.join(TESTDATA_OUTPUT_DIR, f"{entity}.json")
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2, default=default_serializer)
        log(f"✅ Generated test data for {entity} at {json_path}")

def generate_excel_dump():
    all_dfs = []
    for entity, config in entities.items():
        data = config.get("sample_data", [])
        df = pd.DataFrame(data)
        all_dfs.append((entity, df))

    os.makedirs(TESTDATA_OUTPUT_DIR, exist_ok=True)
    with pd.ExcelWriter(EXCEL_OUTPUT_FILE, engine="xlsxwriter") as writer:
        for name, df in all_dfs:
            df.to_excel(writer, sheet_name=name, index=False)
    log(f"✅ Excel dump generated at {EXCEL_OUTPUT_FILE}")

def generate_pages_config():
    os.makedirs(PAGES_OUTPUT_DIR, exist_ok=True)

    for root, dirs, files in os.walk(CLIENT_DIR):
        for file in files:
            src_file = os.path.join(root, file)
            relative_path = os.path.relpath(src_file, CLIENT_DIR)
            dest_file = os.path.join(PAGES_OUTPUT_DIR, relative_path)

            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy2(src_file, dest_file)
            log(f"✅ Copied {relative_path} to frontend at {os.path.abspath(dest_file)}")

def generate_test_cases_from_mock(entities, test_dir):
    os.makedirs(test_dir, exist_ok=True)

    for entity_name, config in entities.items():
        if not config.get("fields") or not config.get("sample_data"):
            print(f"⚠️ Skipping test generation for {entity_name} (no fields or mock data)")
            continue

        test_data_list = config.get("sample_data", [])
        if not test_data_list:
            print(f"⚠️ No sample data for {entity_name}")
            continue
        test_data = test_data_list[0]

        test_code = f'''from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_{entity_name}():
    payload = {pprint.pformat(test_data, indent=4)}

    response = client.post("/api/{entity_name}", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") == True

def test_list_{entity_name}():
    response = client.get("/api/{entity_name}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_{entity_name}_options():
    response = client.get("/api/{entity_name}/options")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
'''

        test_file = os.path.join(test_dir, f"test_{entity_name}.py")
        with open(test_file, "w") as f:
            f.write(test_code)

        print(f"✅ Test case generated for {entity_name} at {test_file}")

def copy_entity_files():
    client_dir = os.path.join(CLIENTS_DIR, CLIENT_NAME)
    backend_client_dir = os.path.join(ROOT_DIR, "backend", "clients", CLIENT_NAME)

    os.makedirs(backend_client_dir, exist_ok=True)

    for fname in ["entities.py", "elastic_entities.py"]:
        src = os.path.join(client_dir, fname)
        dst = os.path.join(backend_client_dir, fname)
        if os.path.exists(src):
            shutil.copyfile(src, dst)
            print(f"✅ Copied {fname} to backend client folder.")
        else:
            print(f"⚠️  {fname} not found in client folder.")

def reset_client_code():
    log(f"🚀 Starting code generation for client: {CLIENT_NAME}")
    log(f"📁 Using config: {client_config}")
    generate_models()
    generate_mock_data()
    generate_test_data()
    generate_excel_dump()
    generate_pages_config()
    generate_test_cases_from_mock(entities, TESTS_OUTPUT_DIR)
    copy_entity_files()
    log("🎉 Code generation completed")

if __name__ == "__main__":
    reset_client_code()
