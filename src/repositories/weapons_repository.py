from abstracts.abc_product_repository import AbcProductRepository
from abstracts.abc_property_repository import AbcPropertyRepository
from abstracts.abc_weapons_repository import AbcWeaponsRepository
from sqlalchemy.orm import Session
from repositories.product_repository import ProductRepository
from repositories.property_repository import PropertyRepository

class SqlDbWeaponsRepository(AbcWeaponsRepository):

    def __init__(self, db: Session):
        self.db = db

    @property
    def product_repository(self) ->AbcProductRepository:
        return ProductRepository(self.db)

    @property
    def property_repository(self) ->AbcPropertyRepository:
        return PropertyRepository(self.db)