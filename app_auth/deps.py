from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from schemas import User, TokenData
from infrastructures import *
from jwt_const import *
import jwt
from jwt.exceptions import InvalidTokenError
from utils import get_user
from auth_db import auth_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    user = get_user(auth_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)],):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
