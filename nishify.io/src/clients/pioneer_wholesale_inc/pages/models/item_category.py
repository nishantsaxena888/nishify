from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, date

from backend.utils.db_base import Base

class ItemCategory(Base):
    __tablename__ = 'item_category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)