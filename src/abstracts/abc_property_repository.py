from abc import ABC, abstractmethod
from models.property import Property
from schemas.property_schema import PropertySchema

class AbcPropertyRepository(ABC):

    @abstractmethod
    def r_add_new_property(self, _property: Property):
        raise NotImplementedError

    @abstractmethod
    def r_modify_property(self, id: int, request: PropertySchema):
        raise NotImplementedError

    @abstractmethod
    def r_get_all(self):
        raise NotImplementedError