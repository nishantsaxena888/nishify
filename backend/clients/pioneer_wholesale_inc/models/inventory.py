from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.utils.db_base import Base

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id.id'))
    item = relationship("Item")
    location_id = Column(Integer, ForeignKey('inventory_location.id.id'))
    inventory_location = relationship("Inventory_location")
    quantity = Column(Integer)