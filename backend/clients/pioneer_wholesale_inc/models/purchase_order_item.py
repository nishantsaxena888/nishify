from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Purchase_order_item(Base):
    __tablename__ = 'purchase_order_item'
    po_id = Column(Integer, ForeignKey('purchase_order.id'))
    item_id = Column(Integer, ForeignKey('item.id'))
    quantity = Column(Integer)
    unit_price = Column(Float)