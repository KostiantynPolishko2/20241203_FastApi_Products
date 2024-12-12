from abstracts.abc_weapons_repository import AbcWeaponsRepository
from models.product import Product

class ProductService:

    def __init__(self, weapons_repository: AbcWeaponsRepository):
        self.weapons_repository = weapons_repository

    def get_all(self):
        return self.weapons_repository.get_all()

    def get_product_card_by_name(self, model: str):
        return self.weapons_repository.get_product_card_by_name(model.lower())

    def delete_product_by_name(self, model: str):
        self.weapons_repository.delete_product_by_name(model.lower())

    def delete_product(self, product: Product):
        self.weapons_repository.delete_product(product)

    def add_new_product(self, product: Product)->int:
        return self.weapons_repository.add_new_product(product)