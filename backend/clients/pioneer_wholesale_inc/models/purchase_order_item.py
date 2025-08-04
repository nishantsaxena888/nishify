from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.utils.db_base import Base

class Purchase_order_item(Base):
    __tablename__ = 'purchase_order_item'
    po_id = Column(Integer, ForeignKey('purchase_order.id.id'), primary_key=True)
    purchase_order = relationship("Purchase_order")
    item_id = Column(Integer, ForeignKey('item.id.id'), primary_key=True)
    item = relationship("Item")
    quantity = Column(Integer)
    unit_price = Column(Float)