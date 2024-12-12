from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from repositories.product_repository import *
from services.product_service import ProductService

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