from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date

from backend.utils.db_base import Base

class InventoryLocation(Base):
    __tablename__ = 'inventory_location'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)