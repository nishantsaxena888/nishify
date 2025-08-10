from fastapi import APIRouter, HTTPException, Query, Depends, Request
from backend.search_elastic.query import search_elastic
from backend.utils.config import get_elastic_config

elastic_entities = get_elastic_config()

from sqlalchemy import select, insert, update, delete, func, and_
from sqlalchemy.orm import Session
from backend.utils.db import get_db
from backend.utils.model_loader import get_model_class
from backend.utils.pydantic_model import create_pydantic_model
from backend.utils.pagination import apply_pagination, paginated_response
from backend.utils.filtering import parse_filter_expression
from typing import Optional
from sqlalchemy import Integer, Float, String, Boolean, Date, DateTime, Numeric  # add at top if not present



def generate_entity_router(client_name: str):
    router = APIRouter()
    def _sa_type_to_kind(col) -> str:
        t = col.type
        if isinstance(t, Integer):   return "int"
        if isinstance(t, Float):     return "float"
        if isinstance(t, Boolean):   return "bool"
        if isinstance(t, Date):      return "date"
        if isinstance(t, DateTime):  return "datetime"
        if isinstance(t, Numeric):   return "decimal"
        if isinstance(t, String):    return "str"
        return "str"

    @router.get("/{entity}/options")
    def get_entity_options(entity: str, schema: str = Query("min", pattern="^(min|full)$")):
        model = get_model_class(client_name, entity)
        cols = list(model.__table__.columns)

        # keep current behavior
        if schema == "min":
            return [c.name for c in cols]

        # rich schema
        fields = []
        for c in cols:
            # FK like "item.id"
            fk = None
            if c.foreign_keys:
                fkcol = next(iter(c.foreign_keys)).column
                fk = f"{fkcol.table.name}.{fkcol.name}"

            default_val = None
            if c.default is not None:
                try:
                    default_val = c.default.arg
                except Exception:
                    default_val = None

            fields.append({
                "name": c.name,
                "type": _sa_type_to_kind(c),
                "label": c.name.replace("_", " ").title(),
                "required": (not c.nullable) and (not c.primary_key),
                "read_only": bool(c.primary_key),
                "nullable": bool(c.nullable),
                "primary_key": bool(c.primary_key),
                "foreign_key": fk,
                "default": default_val,
            })

        pk = next((c.name for c in cols if c.primary_key), None)
        return {
            "entity": entity,
            "title": entity.replace("_", " ").title(),
            "primary_key": pk,
            "fields": fields,
            # simple defaults; your UI can override if it has layout config
            "form": {"sections": [{"title": "Main", "fields": [c.name for c in cols if not c.primary_key]}]},
            "list": {"columns": [c.name for c in cols]},
        }

    @router.get("/{entity}")
    def list_entities(
        entity: str,
        request: Request,
        page: int = Query(1, ge=1),
        size: int = Query(20, le=100),
        db: Session = Depends(get_db),
    ):
        model = get_model_class(client_name, entity)
        raw_query_params = dict(request.query_params)
        raw_query_params.pop("page", None)
        raw_query_params.pop("size", None)

        # ✅ Use Elasticsearch if entity is indexed
        if entity in elastic_entities:

            print(f"[🔍 ElasticSearch] Fetching entity from index: {entity}")
            results = search_elastic(entity, raw_query_params, page, size)
            return paginated_response(results["items"], page, size, results["total"])
        print(f"[🗃️ SQLAlchemy] Fetching entity from SQL table: {entity}")
        # ✅ Else fallback to SQLAlchemy
        filters = []
        for field, value in raw_query_params.items():
            expr = parse_filter_expression(field, value, model)
            if expr is not None:
                filters.append(expr)

        stmt = select(model)
        if filters:
            stmt = stmt.where(and_(*filters))

        count_stmt = select(func.count()).select_from(model)
        if filters:
            count_stmt = count_stmt.where(and_(*filters))

        stmt = apply_pagination(stmt, page, size)

        total = db.scalar(count_stmt)
        items = db.execute(stmt).scalars().all()
        return paginated_response(items, page, size, total)


























    @router.get("/{entity}/{item_id}")
    def get_one(entity: str, item_id: int, db: Session = Depends(get_db)):
        model = get_model_class(client_name, entity)
        result = db.get(model, item_id)
        if not result:
            raise HTTPException(status_code=404, detail="Item not found")
        return result

    @router.post("/{entity}")
    async def create_entity(entity: str, request: Request, db: Session = Depends(get_db)):
        model = get_model_class(client_name, entity)
        schema = create_pydantic_model(model)
        payload = schema(**(await request.json()))
        stmt = insert(model).values(**payload.dict())
        db.execute(stmt)
        db.commit()
        return {"success": True}

    @router.put("/{entity}/{item_id}")
    async def update_entity(entity: str, item_id: int, request: Request, db: Session = Depends(get_db)):
        model = get_model_class(client_name, entity)
        schema = create_pydantic_model(model)
        payload = schema(**(await request.json()))
        stmt = update(model).where(model.id == item_id).values(**payload.dict())
        db.execute(stmt)
        db.commit()
        return {"success": True}

    @router.delete("/{entity}/{item_id}")
    def delete_entity(entity: str, item_id: int, db: Session = Depends(get_db)):
        model = get_model_class(client_name, entity)
        stmt = delete(model).where(model.id == item_id)
        db.execute(stmt)
        db.commit()
        return {"success": True}

    return router
