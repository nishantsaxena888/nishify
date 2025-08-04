from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.utils.db_base import Base

class Cash_discount_group(Base):
    __tablename__ = 'cash_discount_group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    discount_percent = Column(Float)
    terms = Column(String)