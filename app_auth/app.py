from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated, Dict
from deps import get_current_active_user
from schemas import User, Token
from infrastructures import auth_exceptions
from jwt_const import *
from utils import authenticate_user, create_access_token
from auth_db import auth_db
from datetime import timedelta

app = FastAPI()

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()])->Token:
    user = authenticate_user(auth_db, form_data.username, form_data.password)
    if not user:
        raise auth_exceptions

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@app.get("/user/{model}")
async def read_user(model:str, current_user: Annotated[User, Depends(get_current_active_user)])->str:
    return f'read product model {model}'
