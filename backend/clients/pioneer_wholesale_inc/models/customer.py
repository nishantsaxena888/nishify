from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.utils.db_base import Base

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)
    phone = Column(String)
    salesperson_id = Column(Integer, ForeignKey('salesperson.id.id'))
    salesperson = relationship("Salesperson")
    credit_limit = Column(Float)