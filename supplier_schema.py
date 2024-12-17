from redis_om import HashModel, Field
from pydantic import BaseModel, field_validator

class SupplierSchema(HashModel):
    name: str=Field(index=True)
    budget: float=Field(ge=100)

class SupplierSchemaInput(BaseModel):
    name: str
    budget: float

    @field_validator('name')
    def set_name_lowercase(cls, value: str):
        if value:
            return value.lower()
        return value

class SupplierSchemaPublic(SupplierSchemaInput):
    id: int = Field(default=0)

    # Configure the model to allow validation from SQLAlchemy attributes
    model_config = {
        'from_attributes': True
    }