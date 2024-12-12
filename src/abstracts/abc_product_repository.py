from abc import ABC, abstractmethod

class AbcProductRepository(ABC):
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError