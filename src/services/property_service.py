from models.property import Property
from abstracts.abc_property_repository import AbcPropertyRepository
from schemas.property_schema import PropertySchema
from schemas.property_schema_dto import PropertySchemaDto
from schemas.enum_schema import EnumAvailable

class PropertyService:

    def __init__(self, property_repository: AbcPropertyRepository):
        self.property_repository = property_repository

    def s_add_new_property(self, _property: Property):
        self.property_repository.r_add_new_property(_property)

    def s_modify_property(self, id: int, request: PropertySchema):
        self.property_repository.r_modify_property(id, request)

    def s_get_all_available(self, is_available: str):
        props: list[type[Property]] = self.property_repository.r_get_all()
        props_dto: list[PropertySchemaDto] = []

        if is_available != EnumAvailable.all:
            for prop in props:
                if prop.is_available == (is_available == 'yes'):
                    props_dto.append(PropertySchemaDto(price=prop.price, available='yes' if prop.is_available else 'no', description=prop.description))
            return props_dto

        for prop in props:
            props_dto.append(PropertySchemaDto(price=prop.price, available='yes' if prop.is_available else 'no', description=prop.description))

        return props_dto