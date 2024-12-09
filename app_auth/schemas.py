from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from fastapi import Form
from typing import Annotated

class User(BaseModel):
    username: str = Field(min_length=5, max_length=12, description='login')
    email: EmailStr
    is_disabled: bool=Field(default=False, description="users' status")

class UserAuth(User):
    password: str = Field(min_length=5, max_length=12, description='login')

class UserInDB(User):
    guid: UUID
    hashed_password: str

class UserOut(BaseModel):
    guid: UUID
    email: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Custom OAuth2PasswordRequestForm
class CustomOAuth2PasswordRequestForm:
    def __init__(
        self,
        username: str = Form(..., description="The user's username", min_length=5, max_length=10),
        password: str = Form(..., description="The user's password")
    ):
        self.username = username
        self.password = password

#===================schema entities of Response===================#
class ProductSchemaResponse(BaseModel):
    code: int
    status: str
    property: str

    def __str__(self):
        return f'{self.code}:{self}, {self.property}'
