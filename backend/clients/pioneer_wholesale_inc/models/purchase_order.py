from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.utils.db_base import Base

class Purchase_order(Base):
    __tablename__ = 'purchase_order'
    id = Column(Integer, primary_key=True)
    vendor_id = Column(Integer, ForeignKey('vendor.id.id'))
    vendor = relationship("Vendor")
    date = Column(DateTime)
    status = Column(String)