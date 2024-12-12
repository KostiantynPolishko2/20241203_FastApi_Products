from models.product import Product
from sqlalchemy.orm import Session
from infrastructures.product_exception import *
from abstracts.abc_weapons_repository import AbcWeaponsRepository
from schemas.product_schema import ProductSchemaPublic

class SqlDbWeaponsRepository(AbcWeaponsRepository):

    def __init__(self, db: Session):
        self.db=db

    def get_all(self):
        products = self.db.query(Product).all()
        if not products:
            raise products_empty

        return products
