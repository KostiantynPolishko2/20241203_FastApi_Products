from fastapi import FastAPI, Depends, status
from fastapi.responses import RedirectResponse
# from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from deps import get_current_active_user
from schemas import *
from infrastructures import auth_exceptions, create_user_exceptions
from jwt_const import *
from utils import authenticate_user, create_access_token, get_password_hash
from datetime import timedelta
from uuid import uuid4
from database import get_db
from sqlalchemy.orm import Session
from models import UserModel

app = FastAPI()

def map_property_orm_schema_to_sql(request: UserModel, orm_model_class: type[UserInDB])->UserInDB:
    return orm_model_class(**request.model_dump())

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

@app.post('/signup', summary="register new user", status_code=status.HTTP_201_CREATED)
async def create_user(request: UserAuth, db: Annotated[Session, Depends(get_db)])->ProductSchemaResponse:

    # querying database to check if user already exist
    user = db.query(UserModel).filter(UserModel.username == request.username.lower()).first()
    if user is not None:
            raise create_user_exceptions

    new_user = UserModel(
        username=request.username,
        email=request.email,
        is_disabled=request.is_disabled,
        guid=uuid4(),
        hashed_password=get_password_hash(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return ProductSchemaResponse(code=status.HTTP_201_CREATED, status='created', property=f'username: {new_user.username}')

@app.post("/token")
async def login(form_data: Annotated[CustomOAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)])->Token:
    user: UserModel = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise auth_exceptions

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@app.get("/user/{model}")
async def read_user(model:str, authorization: Annotated[User, Depends(get_current_active_user)])->str:
    return f'read product model {model}'
