from abstracts.abc_weapons_repository import AbcWeaponsRepository
from models.property import Property
from abstracts.abc_property_repository import AbcPropertyRepository

class PropertyService:

    def __init__(self, property_repository: AbcPropertyRepository):
        self.property_repository = property_repository

    def s_add_new_property(self, _property: Property):
        self.property_repository.add_new_property(_property)