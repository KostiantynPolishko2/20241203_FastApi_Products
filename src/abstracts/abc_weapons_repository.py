from abc import ABC, abstractmethod
from models.product import Product
from models.property import Property
from schemas.product_schema import ProductSchema, ProductSchemaModify

class AbcWeaponsRepository(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    def get_product_card_by_name(self, model: str):
        raise NotImplementedError

    def delete_product_by_name(self, model: str):
        raise NotImplementedError

    def add_new_product(self, product: Product)->int:
        raise NotImplementedError

    def delete_product(self, product: Product):
        raise NotImplementedError

    def add_new_property(self, _property: Property):
        raise NotImplementedError

    def update_product(self, model: str, request: ProductSchema):
        raise NotImplementedError

    def modify_product(self, model: str, request: ProductSchemaModify):
        raise NotImplementedError