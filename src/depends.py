from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from repositories.product_repository import *

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_product_repository(db: Annotated[Session, Depends(get_db)]):
    yield ProductRepositorySqlDbWeapons(db)