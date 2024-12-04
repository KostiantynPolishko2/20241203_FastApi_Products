from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base
import enum

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, unique=True)
    category = Column(String)

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    is_avaible = Column(Boolean, name='availability', default=True)
    description = Column(String(100), nullable=True)