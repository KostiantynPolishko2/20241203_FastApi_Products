from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from schemas import User, TokenData
from infrastructures import *
from jwt_const import *
import jwt
from jwt.exceptions import InvalidTokenError
from utils import get_user
from database import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/token')

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db:Annotated[Session, Depends(get_db)]):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)],):
    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
