from pydantic import BaseModel, Field, field_validator

class PropertySchema(BaseModel):
    price: float = Field(gt=1000)
    is_available: bool = Field(default=True)
    description: str | None = Field(max_length=100)

    @field_validator('description')
    def set_category_lowercase(cls, value: str)->str:
        if value:
            return value.lower()
        return value

class PropertySchemaPublic(PropertySchema):
    id: int

class PropertySchemaInput(PropertySchema):
    product_id: int = Field(default=0)

    @classmethod
    def from_property(cls, _property: PropertySchema, product_id: int):
        return cls(price=_property.price,
                   is_available=_property.is_available,
                   description=_property.description,
                   product_id=product_id
                   )