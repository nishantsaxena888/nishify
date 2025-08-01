from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Invoice_item(Base):
    __tablename__ = 'invoice_item'
    invoice_id = Column(Integer, ForeignKey('invoice.id'))
    item_id = Column(Integer, ForeignKey('item.id'))
    quantity = Column(Integer)