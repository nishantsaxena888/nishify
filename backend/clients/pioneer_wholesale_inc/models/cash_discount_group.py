from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Cash_discount_group(Base):
    __tablename__ = 'cash_discount_group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    discount_percent = Column(Float)
    terms = Column(String)