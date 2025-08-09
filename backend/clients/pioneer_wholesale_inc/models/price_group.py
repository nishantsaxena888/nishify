from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date

from backend.utils.db_base import Base

class PriceGroup(Base):
    __tablename__ = 'price_group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    markup_percent = Column(Float)