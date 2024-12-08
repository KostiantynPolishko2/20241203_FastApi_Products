from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from fastapi import Form
from typing import Annotated

class User(BaseModel):
    username: str = Field(min_length=5, max_length=12, description='login')
    email: EmailStr
    is_disabled: bool=Field(default=False, description="users' status")

class UserAuth(User):
    password: str

class UserInDB(User):
    id: UUID
    hashed_password: str

class UserOut(BaseModel):
    id: UUID
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
