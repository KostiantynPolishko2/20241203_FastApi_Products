from pydantic import BaseModel, Field

class ResponseSchema(BaseModel):
    code: int
    status: str
    property: str

    def __str__(self):
        return f'{self.code}:{self}, {self.property}'