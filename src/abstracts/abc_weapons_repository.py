from abc import ABC, abstractmethod
from abstracts.abc_product_repository import AbcProductRepository
from abstracts.abc_property_repository import AbcPropertyRepository

class AbcWeaponsRepository(ABC):
    @property
    @abstractmethod
    def product_repository(self)->AbcProductRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def property_repository(self)->AbcPropertyRepository:
        raise NotImplementedError