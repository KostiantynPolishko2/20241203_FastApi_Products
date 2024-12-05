from pydantic import BaseModel, Field

#===================schema entities of Property===================#
class PropertySchema(BaseModel):
    price: float = Field(gt=1000)
    is_available: bool = Field(default=True)
    description: str | None = Field(max_length=100)

class PropertySchemaPublic(PropertySchema):
    id: int


#===================schema entities of Product===================#
class ProductSchema(BaseModel):
    model: str = Field(description='weapons model', min_length=2, max_length=12)
    category: str

class ProductSchemaPublic(ProductSchema):
    id: int

class ProductSchemaModify(BaseModel):
    category: str = Field(description='weapons model', min_length=2, max_length=12)

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

#===================schema entities of Responce===================#
class ProductSchemaResponse(BaseModel):
    code: int
    status: str
    property: str

    def __str__(self):
        return f'{self.code}:{self}, {self.property}'
