from abc import ABC, abstractmethod
from models.product import Product
from schemas.product_schema import ProductSchema, ProductSchemaModify

class AbcProductRepository(ABC):

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_product_card_by_name(self, model: str):
        raise NotImplementedError

    @abstractmethod
    def delete_product_by_name(self, model: str):
        raise NotImplementedError

    @abstractmethod
    def add_new_product(self, product: Product)->int:
        raise NotImplementedError

    @abstractmethod
    def delete_product(self, product: Product):
        raise NotImplementedError

    @abstractmethod
    def update_product(self, model: str, request: ProductSchema):
        raise NotImplementedError

    @abstractmethod
    def modify_product(self, model: str, request: ProductSchemaModify):
        raise NotImplementedError