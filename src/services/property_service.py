from models.property import Property
from abstracts.abc_property_repository import AbcPropertyRepository
from schemas.property_schema import PropertySchema

class PropertyService:

    def __init__(self, property_repository: AbcPropertyRepository):
        self.property_repository = property_repository

    def s_add_new_property(self, _property: Property):
        self.property_repository.r_add_new_property(_property)

    def s_modify_property(self, id: int, request: PropertySchema):
        self.property_repository.r_modify_property(id, request)