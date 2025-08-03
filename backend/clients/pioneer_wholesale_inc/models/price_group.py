from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime

from backend.utils.db_base import Base

class Price_group(Base):
    __tablename__ = 'price_group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    markup_percent = Column(Float)