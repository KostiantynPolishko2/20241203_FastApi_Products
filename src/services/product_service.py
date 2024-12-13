from abstracts.abc_weapons_repository import AbcWeaponsRepository
from models.product import Product
from schemas.product_schema import ProductSchema, ProductSchemaModify
from abstracts.abc_product_repository import AbcProductRepository

class ProductService:

    def __init__(self, product_repository: AbcProductRepository):
        self.product_repository = product_repository

    def get_all(self):
        return self.product_repository.get_all()

    def get_product_card_by_name(self, model: str):
        return self.product_repository.get_product_card_by_name(model.lower())

    def delete_product_by_name(self, model: str):
        self.product_repository.delete_product_by_name(model.lower())

    def delete_product(self, product: Product):
        self.product_repository.delete_product(product)

    def add_new_product(self, product: Product)->int:
        return self.product_repository.add_new_product(product)

    def update_product(self, model: str, request: ProductSchema):
        self.product_repository.update_product(model.lower(), request)

    def modify_product(self, model: str, request: ProductSchemaModify):
        self.product_repository.modify_product(model.lower(), request)