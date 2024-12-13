from abc import ABC, abstractmethod
from models.property import Property

class AbcPropertyRepository(ABC):
    @abstractmethod
    def add_new_property(self, _property: Property):
        raise NotImplementedError