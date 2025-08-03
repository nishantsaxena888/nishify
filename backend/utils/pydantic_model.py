from pydantic import BaseModel, create_model
from typing import Any
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeMeta

def create_pydantic_model(model: DeclarativeMeta) -> BaseModel:
    fields = {
        col.name: (col.type.python_type, ...)
        for col in model.__table__.columns
        if col.name != "id"  # skip PK if needed
    }
    return create_model(f"{model.__name__}Schema", **fields)
