from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, date
from backend.clients.pioneer_wholesale_inc.models.vendor import Vendor

from backend.utils.db_base import Base

class PurchaseOrder(Base):
    __tablename__ = 'purchase_order'
    id = Column(Integer, primary_key=True)
    vendor_id = Column(Integer, ForeignKey('vendor.id'))
    date = Column(DateTime)
    status = Column(String)
    vendor = relationship('Vendor')