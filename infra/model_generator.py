import os
from infra.pioneer_wholesale_inc.entities import entities
from datetime import datetime
import json
import pandas as pd

# Define key directories
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
MODEL_OUTPUT_DIR = os.path.join(BASE_DIR, "backend/models")
MOCK_OUTPUT_DIR = os.path.join(BASE_DIR, "nishify.io/src/mocks")
TESTDATA_OUTPUT_DIR = os.path.join(BASE_DIR, "backend/test_data")
EXCEL_OUTPUT_FILE = os.path.join(TESTDATA_OUTPUT_DIR, "test_data.xlsx")

def type_map(field_type):
    """
    Map simplified field types to SQLAlchemy types.

    Args:
        field_type (str): The field type (e.g., 'int', 'str', etc.)

    Returns:
        str: SQLAlchemy type as string
    """
    return {
        "int": "Integer",
        "str": "String",
        "float": "Float",
        "bool": "Boolean",
        "datetime": "DateTime",
    }.get(field_type, "String")

def generate_models():
    """
    Generate SQLAlchemy model files for each entity.
    Fields are derived from the `entities` config.

    Example:
        id = Column(Integer, primary_key=True)
        name = Column(String, nullable=False)
    """
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
            line = f"    {field_name} = Column({sql_type}, {', '.join(opts)})"
            lines.append(line)

        model_code = "\n".join(lines)
        with open(os.path.join(MODEL_OUTPUT_DIR, f"{entity}.py"), "w") as f:
            f.write(model_code)
        print(f"✅ Generated model for {entity}")

def generate_mock_data():
    """
    Generate mock API handlers in TypeScript for frontend mocking.

    Each entity will have:
      - options(): returns list of fields
      - get(): returns sample data array
      - getOne(id): returns first sample row
      - post(payload): adds a random ID
      - update(payload): returns payload as is
    """
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

        with open(os.path.join(MOCK_OUTPUT_DIR, f"{entity}.ts"), "w") as f:
            f.write("\n".join(lines))
        print(f"✅ Generated mock for {entity}")

def generate_test_data():
    """
    Generate static test data for backend unit tests.

    Output:
      backend/test_data/<entity>.json
    """
    os.makedirs(TESTDATA_OUTPUT_DIR, exist_ok=True)

    for entity, config in entities.items():
        data = config.get("sample_data", [])
        with open(os.path.join(TESTDATA_OUTPUT_DIR, f"{entity}.json"), "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Generated test data for {entity}")

def generate_excel_dump():
    """
    Create a multi-sheet Excel file where each sheet is one entity's sample data.

    Output:
      backend/test_data/test_data.xlsx
    """
    all_dfs = []
    for entity, config in entities.items():
        data = config.get("sample_data", [])
        df = pd.DataFrame(data)
        all_dfs.append((entity, df))

    os.makedirs(TESTDATA_OUTPUT_DIR, exist_ok=True)
    with pd.ExcelWriter(EXCEL_OUTPUT_FILE, engine="xlsxwriter") as writer:
        for name, df in all_dfs:
            df.to_excel(writer, sheet_name=name, index=False)
    print(f"✅ Excel dump generated at {EXCEL_OUTPUT_FILE}")

def reset_client_code():
    """
    Master function to regenerate all components for a client:
      - SQLAlchemy models
      - Frontend mocks
      - Backend test JSON
      - Excel data snapshot
    """
    generate_models()
    generate_mock_data()
    generate_test_data()
    generate_excel_dump()

if __name__ == "__main__":
    reset_client_code()
