from abstracts.abc_weapons_repository import AbcWeaponsRepository
from schemas.product_schema import ProductSchemaPublic

class ProductService:

    def __init__(self, weapons_repository: AbcWeaponsRepository):
        self.weapons_repository = weapons_repository

    def get_all(self):
        return self.weapons_repository.get_all()