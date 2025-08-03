from fastapi import APIRouter, HTTPException, Query, Depends, Request
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from backend.utils.db import get_db
from backend.utils.model_loader import get_model_class
from backend.utils.pydantic_model import create_pydantic_model
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
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 50,
        search: Optional[str] = None
    ):
        model = get_model_class(client_name, entity)
        stmt = select(model).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

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
