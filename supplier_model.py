from sqlalchemy import Column, Integer, Float, String, UniqueConstraint, CheckConstraint
from database import Base, engine

class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    budget = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint('name', name='uq_supplier_name'),
        CheckConstraint('budget >= 100', name='ck_budget_minimum')
    )

Base.metadata.create_all(bind=engine)