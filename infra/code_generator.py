import os
import importlib.util
from datetime import datetime
import json
import pandas as pd
import sys

LOG = True

# ✅ Accept client name as argument
if len(sys.argv) < 2:
    raise ValueError("Client name must be passed as an argument. Usage: python code_generator.py <client_name>")

CLIENT_NAME = sys.argv[1]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))  # Treat nishify/ as root

MODEL_OUTPUT_DIR = os.path.join(ROOT_DIR, f"backend/clients/{CLIENT_NAME}/models")
MOCK_OUTPUT_DIR = os.path.join(ROOT_DIR, f"nishify.io/src/lib/api/mock/{CLIENT_NAME}")
TESTDATA_OUTPUT_DIR = os.path.join(ROOT_DIR, f"backend/clients/{CLIENT_NAME}/test_data")
EXCEL_OUTPUT_FILE = os.path.join(TESTDATA_OUTPUT_DIR, "test_data.xlsx")

# 🔁 Dynamic import of entities.py from client folder
ENTITIES_PATH = os.path.join(SCRIPT_DIR, f"{CLIENT_NAME}/entities.py")
spec = importlib.util.spec_from_file_location("entities", ENTITIES_PATH)
entities_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entities_module)
entities = entities_module.entities

def log(msg):
    if LOG:
        print(msg)

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
        lines = [
            "from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey",
            "from sqlalchemy.ext.declarative import declarative_base",
            "from datetime import datetime",
            "\nBase = declarative_base()",
            f"\nclass {entity.capitalize()}(Base):",
            f"    __tablename__ = '{entity}'",
        ]

        for field_name, field_conf in fields.items():
            sql_type = type_map(field_conf["type"])
            opts = []
            if field_conf.get("primary_key"):
                opts.append("primary_key=True")
            if field_conf.get("required"):
                opts.append("nullable=False")
            if field_conf.get("auto_now"):
                opts.append("default=datetime.utcnow")
            if field_conf.get("foreign_key"):
                opts.append(f"ForeignKey('{field_conf['foreign_key']}')")
            line = f"    {field_name} = Column({sql_type}{', ' + ', '.join(opts) if opts else ''})"
            lines.append(line)

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
            json.dump(data, f, indent=2)
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

def reset_client_code():
    log(f"🚀 Starting code generation for client: {CLIENT_NAME}")
    generate_models()
    generate_mock_data()
    generate_test_data()
    generate_excel_dump()
    log("🎉 Code generation completed")

if __name__ == "__main__":
    reset_client_code()
