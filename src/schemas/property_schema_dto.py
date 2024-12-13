from pydantic import BaseModel, Field, field_validator

class PropertySchemaDto(BaseModel):
    price: float
    available: str = Field(default='yes')
    description: str

    @field_validator('description')
    @classmethod
    def set_description_capitalize(cls, value: str)->str:
        if value:
            return cls.srt_capitalize(value)
        return value

    @staticmethod
    def srt_capitalize(text: str)->str:
        sentences = list(text.split('. '))
        sentences[0].capitalize()

        for i in range(1, len(sentences)):
            sentences[i] = sentences[i].capitalize()

        return '. '.join(sentences)