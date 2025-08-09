from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date
from backend.clients.pioneer_wholesale_inc.models.salesperson import Salesperson

from backend.utils.db_base import Base

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)
    phone = Column(String)
    salesperson_id = Column(Integer, ForeignKey('salesperson.id'))
    credit_limit = Column(Float)
    salesperson = relationship('Salesperson')