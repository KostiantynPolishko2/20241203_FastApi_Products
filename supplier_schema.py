from redis_om import HashModel, Field
from pydantic import BaseModel
# from redis_config import redis

class SupplierSchema(HashModel):
    name: str=Field(index=True)
    budget: float=Field(ge=100)

class SupplierSchemaResponse(BaseModel):
    name: str
    budget: float

    # class Meta:
    #     database = redis