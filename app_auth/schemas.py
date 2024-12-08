from pydantic import BaseModel
from uuid import UUID

class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None

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
