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

def generate_entity_router(client_name: str):
    router = APIRouter()

    @router.get("/{entity}/options")
    def get_entity_options(entity: str):
        model = get_model_class(client_name, entity)
        return [col.name for col in model.__table__.columns]

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
