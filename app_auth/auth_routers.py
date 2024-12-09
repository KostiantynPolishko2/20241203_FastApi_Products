from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
# from fastapi.security import OAuth2PasswordRequestForm
from deps import get_current_active_user
from schemas import *
from infrastructures import auth_exceptions, add_user_exceptions
from jwt_const import *
from utils import authenticate_user, create_access_token
from datetime import timedelta
from database import get_db
from sqlalchemy.orm import Session
from models import UserModel
from auth_repository import AuthRepository

router = APIRouter(
    prefix='/user',
    tags=['Http request: User'],
    responses={status.HTTP_400_BAD_REQUEST: {'description' : 'Bad Request'}}
)

def get_auth_repository(db: Annotated[Session, Depends(get_db)]):
    yield AuthRepository(db)

def map_property_orm_schema_to_sql(request: UserModel, orm_model_class: type[UserInDB])->UserInDB:
    return orm_model_class(**request.model_dump())

@router.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

@router.post('/signup', summary="register new user", status_code=status.HTTP_201_CREATED)
async def create_user(request: UserAuth, auth_repository: Annotated[AuthRepository, Depends(get_auth_repository)])->ProductSchemaResponse:

    auth_repository.is_exist_user(request.username)
    response = auth_repository.add_user_to_db(request)

    if response == 0:
        raise add_user_exceptions

    return ProductSchemaResponse(code=status.HTTP_201_CREATED, status='created', property=f'username: {request.username}')

@router.post("/token")
async def login(form_data: Annotated[CustomOAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)])->Token:
    user: UserModel = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise auth_exceptions

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@router.get("/{username}", deprecated=False)
async def get_username(username: str, authorization: Annotated[User, Depends(get_current_active_user)], auth_repository: Annotated[AuthRepository, Depends(get_auth_repository)]):
    if len(username) <= 5:
        raise ValueError('Argument cannot be null')

    return auth_repository.get_user(username)