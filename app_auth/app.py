from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Dict
from deps import get_current_active_user
from schemas import User, UserInDB
from auth import auth_db
from utils import fake_hash_password

app = FastAPI()

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = auth_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/user/{name}")
async def read_user(name:str, current_user: Annotated[User, Depends(get_current_active_user)])->dict:
    return {name: current_user}

@app.post("/user/{name}")
async def create_user(name:str, current_user: Annotated[User, Depends(get_current_active_user)])->dict:
    return {name: current_user}