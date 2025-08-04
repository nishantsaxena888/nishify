from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.clients.pioneer_wholesale_inc.models.inventory_location import Inventory_location
from backend.clients.pioneer_wholesale_inc.models.item import Item

from backend.utils.db_base import Base

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.id'))
    location_id = Column(Integer, ForeignKey('inventory_location.id'))
    quantity = Column(Integer)
    item = relationship(Item)
    location = relationship(Inventory_location)