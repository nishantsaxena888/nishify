from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, date

from backend.utils.db_base import Base

class CashDiscountGroup(Base):
    __tablename__ = 'cash_discount_group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    discount_percent = Column(Float)
    terms = Column(String)