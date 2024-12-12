from abc import ABC, abstractmethod
from schemas.product_schema import ProductSchemaPublic

class AbcWeaponsRepository(ABC):
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError