from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from utils import fake_decode_token
from schemas import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)])->User:
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)],)->User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
