from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date
from backend.clients.pioneer_wholesale_inc.models.cash_discount_group import CashDiscountGroup
from backend.clients.pioneer_wholesale_inc.models.item_category import ItemCategory
from backend.clients.pioneer_wholesale_inc.models.price_group import PriceGroup
from backend.clients.pioneer_wholesale_inc.models.secondary_category import SecondaryCategory
from backend.clients.pioneer_wholesale_inc.models.tax_group import TaxGroup
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
    category = relationship('ItemCategory')
    secondary_category = relationship('SecondaryCategory')
    vendor = relationship('Vendor')
    tax_group = relationship('TaxGroup')
    price_group = relationship('PriceGroup')
    cash_discount_group = relationship('CashDiscountGroup')