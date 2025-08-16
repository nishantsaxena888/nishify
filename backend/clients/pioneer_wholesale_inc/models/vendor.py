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

class Vendor(Base):
    __tablename__ = "vendor"




    id = Column(
        _sa_type("int"),
        primary_key=True, autoincrement=True    )



    name = Column(
        _sa_type("str"), nullable=False    )



    address = Column(
        _sa_type("str")    )



    email = Column(
        _sa_type("str")    )



    phone = Column(
        _sa_type("str")    )



    contact_person = Column(
        _sa_type("str")    )



    state_id = Column(
        _sa_type("int"),
        ForeignKey("state.id")    )



    state = relationship(
        "State",
        primaryjoin="Vendor.state_id == State.id",
        foreign_keys=[state_id]
    )
