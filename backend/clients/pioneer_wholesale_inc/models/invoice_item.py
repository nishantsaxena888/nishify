from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.utils.db_base import Base

class Invoice_item(Base):
    __tablename__ = 'invoice_item'
    invoice_id = Column(Integer, ForeignKey('invoice.id.id'), primary_key=True)
    invoice = relationship("Invoice")
    item_id = Column(Integer, ForeignKey('item.id.id'), primary_key=True)
    item = relationship("Item")
    quantity = Column(Integer)
    price = Column(Float)