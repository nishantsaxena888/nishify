from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime

from backend.utils.db_base import Base

class Tax_group(Base):
    __tablename__ = 'tax_group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tax_percent = Column(Float)