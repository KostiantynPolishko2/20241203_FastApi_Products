from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from utils import fake_decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user