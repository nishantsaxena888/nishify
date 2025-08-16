from __future__ import annotations
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Date, DateTime,
    ForeignKey, UniqueConstraint, Text
)
from sqlalchemy.orm import relationship
from backend.utils.db import Base

def _sa_type(tname: str):
    t = (tname or "string").lower()
    if t in ("string", "str", "keyword", "varchar"): return String(255)
    if t in ("text",): return Text()
    if t in ("int", "integer"): return Integer()
    if t in ("float", "double", "number", "numeric"): return Float()
    if t in ("bool", "boolean"): return Boolean()
    if t in ("date",): return Date()
    if t in ("datetime", "timestamp"): return DateTime()
    return String(255)

class Inventory(Base):
    __tablename__ = "inventory"




    id = Column(
        _sa_type("int"),
        primary_key=True, autoincrement=True    )



    item_id = Column(
        _sa_type("int"),
        ForeignKey("item.id")    )



    location_id = Column(
        _sa_type("int"),
        ForeignKey("inventory_location.id")    )



    quantity = Column(
        _sa_type("int")    )



    item = relationship(
        "Item",
        primaryjoin="Inventory.item_id == Item.id",
        foreign_keys=[item_id]
    )
    location = relationship(
        "InventoryLocation",
        primaryjoin="Inventory.location_id == InventoryLocation.id",
        foreign_keys=[location_id]
    )
