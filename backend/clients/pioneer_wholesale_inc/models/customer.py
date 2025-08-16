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

class Customer(Base):
    __tablename__ = "customer"



    id = Column(_sa_type("int"), primary_key=True)



    name = Column(_sa_type("str"))



    address = Column(_sa_type("str"))



    email = Column(_sa_type("str"))



    phone = Column(_sa_type("str"))



    salesperson_id = Column(_sa_type("int"), ForeignKey("salesperson.id"))



    credit_limit = Column(_sa_type("float"))

    # Surrogate PK because schema had no pk
    id = Column(String(32), primary_key=True)


    salesperson = relationship(
        "Salesperson",
        primaryjoin="Customer.salesperson_id == Salesperson.id",
        foreign_keys=[salesperson_id]
    )
