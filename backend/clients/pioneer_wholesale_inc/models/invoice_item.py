from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime

from backend.utils.db_base import Base

class Invoice_item(Base):
    __tablename__ = 'invoice_item'
    invoice_id = Column(Integer, ForeignKey('invoice.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    quantity = Column(Integer)
    price = Column(Float)