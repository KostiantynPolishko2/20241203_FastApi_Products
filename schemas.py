from pydantic import BaseModel, Field

class ProductSchema(BaseModel):
    model: str = Field(description='weapons model', min_length=2, max_length=12)
    category: str

class ProductSchemaPublic(ProductSchema):
    id: int