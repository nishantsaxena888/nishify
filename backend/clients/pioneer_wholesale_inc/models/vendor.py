from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date
from backend.clients.pioneer_wholesale_inc.models.state import State

from backend.utils.db_base import Base

class Vendor(Base):
    __tablename__ = 'vendor'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)
    email = Column(String)
    phone = Column(String)
    contact_person = Column(String)
    state_id = Column(Integer, ForeignKey('state.id'))
    state = relationship('State')