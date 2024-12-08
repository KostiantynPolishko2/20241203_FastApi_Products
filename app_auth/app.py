from fastapi import FastAPI, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from deps import get_current_active_user
from schemas import User, Token, UserOut, UserInDB, UserAuth
from infrastructures import auth_exceptions, create_user_exceptions
from jwt_const import *
from utils import authenticate_user, create_access_token, get_password_hash
from auth_db import auth_db
from datetime import timedelta
from uuid import uuid4
from auth_db import auth_db as db

app = FastAPI()

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

@app.post('/signup', summary="register new user", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserAuth)->UserOut:

    # querying database to check if user already exist
    user = db.get(data.username, None)
    if user is not None:
            raise create_user_exceptions

    user = UserInDB(
        username=data.username,
        email=data.email,
        disabled=data.disabled,
        id=uuid4(),
        hashed_password=get_password_hash(data.password)
    )
    db[data.username] = user    # saving user to database

    return user

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()])->Token:
    user = authenticate_user(auth_db, form_data.username, form_data.password)
    if not user:
        raise auth_exceptions

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@app.get("/user/{model}")
async def read_user(model:str, authorization: Annotated[User, Depends(get_current_active_user)])->str:
    return f'read product model {model}'
