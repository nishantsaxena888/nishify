from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.utils.db_base import Base

class Invoice(Base):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id.id'))
    customer = relationship("Customer")
    date = Column(DateTime)
    status = Column(String)