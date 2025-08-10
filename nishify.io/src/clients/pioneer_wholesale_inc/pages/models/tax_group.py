from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, date

from backend.utils.db_base import Base

class TaxGroup(Base):
    __tablename__ = 'tax_group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tax_percent = Column(Float)