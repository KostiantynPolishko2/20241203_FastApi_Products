from pydantic import BaseModel

class ProductSchema(BaseModel):
    model: str
    category: str

class ProductSchemaPublic(ProductSchema):
    id: int