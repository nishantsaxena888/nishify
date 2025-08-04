from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.clients.pioneer_wholesale_inc.models.cash_discount_group import Cash_discount_group
from backend.clients.pioneer_wholesale_inc.models.item_category import Item_category
from backend.clients.pioneer_wholesale_inc.models.price_group import Price_group
from backend.clients.pioneer_wholesale_inc.models.secondary_category import Secondary_category
from backend.clients.pioneer_wholesale_inc.models.tax_group import Tax_group
from backend.clients.pioneer_wholesale_inc.models.vendor import Vendor

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
    category = relationship(Item_category)
    secondary_category = relationship(Secondary_category)
    vendor = relationship(Vendor)
    tax_group = relationship(Tax_group)
    price_group = relationship(Price_group)
    cash_discount_group = relationship(Cash_discount_group)