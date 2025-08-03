from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime

from backend.utils.db_base import Base

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    item_code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('item_category.id'))
    secondary_category_id = Column(Integer, ForeignKey('secondary_category.id'))
    vendor_id = Column(Integer, ForeignKey('vendor.id'))
    tax_group_id = Column(Integer, ForeignKey('tax_group.id'))
    price_group_id = Column(Integer, ForeignKey('price_group.id'))
    cash_discount_group_id = Column(Integer, ForeignKey('cash_discount_group.id'))
    upc_code = Column(String)
    unit = Column(String)
    price = Column(Float)
    description = Column(String)
    active = Column(Boolean)