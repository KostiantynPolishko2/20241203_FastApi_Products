import datetime

from sqlalchemy import Column, Integer, String, Float, Boolean, UniqueConstraint, DATE
from sqlalchemy.orm import DeclarativeBase

from database import Base, engine

# class Base(DeclarativeBase):
#     ...

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, unique=True)
    category = Column(String)

    __table_args__ = (
        UniqueConstraint('model', name='uq_product_model'),  # Named unique constraint
    )

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, name='availability', default=True)
    description = Column(String(100), nullable=True)

Base.metadata.create_all(bind=engine)