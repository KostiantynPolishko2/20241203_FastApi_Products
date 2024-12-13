from pydantic import BaseModel
from models.property import Property
from schemas.property_schema import PropertySchemaInput

class MapHandler(BaseModel):

    @staticmethod
    def props_schema_in_to_props_model(_property: PropertySchemaInput, orm_model_class: type[Property]) -> Property:
        return orm_model_class(**_property.model_dump())