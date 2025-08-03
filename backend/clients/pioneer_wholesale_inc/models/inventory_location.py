from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Inventory_location(Base):
    __tablename__ = 'inventory_location'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)