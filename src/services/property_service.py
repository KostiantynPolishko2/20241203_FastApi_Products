from abstracts.abc_weapons_repository import AbcWeaponsRepository
from models.property import Property

class PropertyService:

    def __init__(self, weapons_repository: AbcWeaponsRepository):
        self.weapons_repository = weapons_repository

    def s_add_new_property(self, _property: Property):
        self.weapons_repository.add_new_property(_property)