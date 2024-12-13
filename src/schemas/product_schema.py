from pydantic import BaseModel, Field, field_validator
from schemas.property_schema import PropertySchema


class ProductSchema(BaseModel):
    model: str = Field(description='weapons model', min_length=2, max_length=12)
    category: str

    @field_validator('model')
    def set_model_lowercase(cls, value: str)->str:
        if value:
            return value.lower()
        return value

    @field_validator('category')
    def set_category_lowercase(cls, value: str)->str:
        if value:
            return value.lower()
        return value

class ProductSchemaPublic(ProductSchema):
    id: int

class ProductSchemaModify(BaseModel):
    category: str = Field(description='weapons model', min_length=2, max_length=12)

    @field_validator('category')
    def set_category_lowercase(cls, value: str)->str:
        if value:
            return value.lower()
        return value

class ProductSchemaProperty(ProductSchema):
    property: PropertySchema

    class Config:
        from_attributes=True

class ProductSchemaCard(BaseModel):
    model: str
    price: float
    description: str

    @classmethod
    def from_property(cls, model:str, _property: PropertySchema):
        return cls(model=model,
                   price=_property.price,
                   description=_property.description)