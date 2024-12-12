from models.product import Product
from sqlalchemy.orm import Session
from infrastructures.product_exception import *
from abstracts.abc_product_repository import AbcProductRepository
from schemas.product_schema import ProductSchemaPublic

class ProductRepositorySqlDbWeapons(AbcProductRepository):

    def __init__(self, db: Session):
        self.db=db

    def get_all(self)->list[ProductSchemaPublic]:
        products = self.db.query(Product).all()
        if not products:
            raise products_empty

        return list[ProductSchemaPublic](products)
