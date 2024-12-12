from sqlalchemy import (Column, Integer, String, UniqueConstraint)
from sqlalchemy.orm import relationship
from databases.database import Base, engine

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, unique=True)
    category = Column(String)
    property = relationship('Property', uselist=False,
                            cascade='all, delete-orphan',   # Enable cascade delete
                            backref='product'   # Optional back-reference from Property to Product
                            )

    __table_args__ = (
        UniqueConstraint('model', name='uq_product_model'),  # Named unique constraint
    )

Base.metadata.create_all(bind=engine)