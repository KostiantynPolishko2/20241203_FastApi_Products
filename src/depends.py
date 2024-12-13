from fastapi import Depends, Path
from typing import Annotated
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
    return ProductService(weapons_repository.product_repository)

def get_property_service(weapons_repository: Annotated[SqlDbWeaponsRepository, Depends(get_sql_weapons_repository)]):
    return PropertyService(weapons_repository.property_repository)

model_params = Annotated[str, Path(description='weapons model', min_length=2)]
product_service = Annotated[ProductService, Depends(get_product_service)]
id_params = Annotated[int, Path(description='id of weapons property', gt=0)]