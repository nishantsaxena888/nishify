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

class InvoiceItem(Base):
    __tablename__ = "invoice_item"



    invoice_id = Column(_sa_type("int"), primary_key=True)



    item_id = Column(_sa_type("int"), primary_key=True)



    quantity = Column(_sa_type("int"))



    price = Column(_sa_type("float"))

    # Surrogate PK because schema had no pk
    id = Column(String(32), primary_key=True)


    invoice = relationship(
        "Invoice",
        primaryjoin="InvoiceItem.invoice_id == Invoice.id",
        foreign_keys=[invoice_id]
    )
    item = relationship(
        "Item",
        primaryjoin="InvoiceItem.item_id == Item.id",
        foreign_keys=[item_id]
    )
