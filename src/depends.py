from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from repositories.weapons_repository import *
from services.product_service import ProductService
from services.property_service import PropertyService

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_sql_weapons_repository(db: Annotated[Session, Depends(get_db)]):
    return SqlDbWeaponsRepository(db)


def get_product_service(weapons_repository: Annotated[SqlDbWeaponsRepository, Depends(get_sql_weapons_repository)]):
    return ProductService(weapons_repository)

def get_property_service(weapons_repository: Annotated[SqlDbWeaponsRepository, Depends(get_sql_weapons_repository)]):
    return PropertyService(weapons_repository)