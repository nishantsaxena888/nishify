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

class Item(Base):
    __tablename__ = "item"



    id = Column(_sa_type("int"), primary_key=True)



    item_code = Column(_sa_type("str"), nullable=False)



    name = Column(_sa_type("str"), nullable=False)



    category_id = Column(_sa_type("int"), ForeignKey("item_category.id"))



    secondary_category_id = Column(_sa_type("int"), ForeignKey("secondary_category.id"))



    vendor_id = Column(_sa_type("int"), ForeignKey("vendor.id"))



    tax_group_id = Column(_sa_type("int"), ForeignKey("tax_group.id"))



    price_group_id = Column(_sa_type("int"), ForeignKey("price_group.id"))



    cash_discount_group_id = Column(_sa_type("int"), ForeignKey("cash_discount_group.id"))



    upc_code = Column(_sa_type("str"))



    unit = Column(_sa_type("str"))



    price = Column(_sa_type("float"))



    description = Column(_sa_type("str"))



    active = Column(_sa_type("bool"))

    # Surrogate PK because schema had no pk
    id = Column(String(32), primary_key=True)


    category = relationship(
        "ItemCategory",
        primaryjoin="Item.category_id == ItemCategory.id",
        foreign_keys=[category_id]
    )
    secondary_category = relationship(
        "SecondaryCategory",
        primaryjoin="Item.secondary_category_id == SecondaryCategory.id",
        foreign_keys=[secondary_category_id]
    )
    vendor = relationship(
        "Vendor",
        primaryjoin="Item.vendor_id == Vendor.id",
        foreign_keys=[vendor_id]
    )
    tax_group = relationship(
        "TaxGroup",
        primaryjoin="Item.tax_group_id == TaxGroup.id",
        foreign_keys=[tax_group_id]
    )
    price_group = relationship(
        "PriceGroup",
        primaryjoin="Item.price_group_id == PriceGroup.id",
        foreign_keys=[price_group_id]
    )
    cash_discount_group = relationship(
        "CashDiscountGroup",
        primaryjoin="Item.cash_discount_group_id == CashDiscountGroup.id",
        foreign_keys=[cash_discount_group_id]
    )
