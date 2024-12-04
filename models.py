from sqlalchemy import Column, Integer, String
from database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, unique=True)
    category = Column(String)
    