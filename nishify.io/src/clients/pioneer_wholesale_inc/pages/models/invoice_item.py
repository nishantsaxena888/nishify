from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, date
from backend.clients.pioneer_wholesale_inc.models.invoice import Invoice
from backend.clients.pioneer_wholesale_inc.models.item import Item

from backend.utils.db_base import Base

class InvoiceItem(Base):
    __tablename__ = 'invoice_item'
    invoice_id = Column(Integer, ForeignKey('invoice.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    quantity = Column(Integer)
    price = Column(Float)
    invoice = relationship('Invoice')
    item = relationship('Item')