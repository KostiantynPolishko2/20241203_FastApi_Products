from sqlalchemy import (Column, Integer, String, Float, Boolean, ForeignKey, ForeignKeyConstraint)
from databases.database import Base, engine

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, name='availability', default=True)
    description = Column(String(100), nullable=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), # Enable CASCADE in DB
                        nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['product_id'], ['products.id'], name='fk_properties_product_id'),
    )

Base.metadata.create_all(bind=engine)