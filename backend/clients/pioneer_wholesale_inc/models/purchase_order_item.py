from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime

from backend.utils.db_base import Base

class Purchase_order_item(Base):
    __tablename__ = 'purchase_order_item'
    po_id = Column(Integer, ForeignKey('purchase_order.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    quantity = Column(Integer)
    unit_price = Column(Float)