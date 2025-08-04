from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.utils.db_base import Base

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    item_code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('item_category.id.id'))
    item_category = relationship("Item_category")
    secondary_category_id = Column(Integer, ForeignKey('secondary_category.id.id'))
    secondary_category = relationship("Secondary_category")
    vendor_id = Column(Integer, ForeignKey('vendor.id.id'))
    vendor = relationship("Vendor")
    tax_group_id = Column(Integer, ForeignKey('tax_group.id.id'))
    tax_group = relationship("Tax_group")
    price_group_id = Column(Integer, ForeignKey('price_group.id.id'))
    price_group = relationship("Price_group")
    cash_discount_group_id = Column(Integer, ForeignKey('cash_discount_group.id.id'))
    cash_discount_group = relationship("Cash_discount_group")
    upc_code = Column(String)
    unit = Column(String)
    price = Column(Float)
    description = Column(String)
    active = Column(Boolean)