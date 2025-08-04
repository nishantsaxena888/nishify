from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.utils.db_base import Base

class Secondary_category(Base):
    __tablename__ = 'secondary_category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)