from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Tax_group(Base):
    __tablename__ = 'tax_group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tax_percent = Column(Float)