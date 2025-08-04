from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.clients.pioneer_wholesale_inc.models.item import Item
from backend.clients.pioneer_wholesale_inc.models.purchase_order import Purchase_order

from backend.utils.db_base import Base

class Purchase_order_item(Base):
    __tablename__ = 'purchase_order_item'
    po_id = Column(Integer, ForeignKey('purchase_order.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    quantity = Column(Integer)
    unit_price = Column(Float)
    po = relationship(Purchase_order)
    item = relationship(Item)