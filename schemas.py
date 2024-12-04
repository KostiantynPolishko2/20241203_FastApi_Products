from pydantic import BaseModel, Field

class ProductSchema(BaseModel):
    model: str = Field(description='weapons model', min_length=2, max_length=12)
    category: str

class ProductSchemaPublic(ProductSchema):
    id: int

class ProductSchemaModify(BaseModel):
    category: str = Field(description='weapons model', min_length=2, max_length=12)

class ProductSchemaResponse(BaseModel):
    code: int
    status: str
    property: str

    def __str__(self):
        return f'{self.code}:{self}, {self.property}'


class PropertySchema(BaseModel):
    price: float = Field(gt=1000)
    is_avaible: bool = Field(default=True)
    description: str | None = Field(max_length=100)

class PropertySchemaPublic(PropertySchema):
    id: int