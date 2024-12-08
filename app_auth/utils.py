from schemas import UserInDB
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from jwt_const import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str)->bool:
    if plain_password.startswith('secret'):
        return f'fake_hashed_{plain_password}' == hashed_password
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str)->str:
    return pwd_context.hash(password)

def get_user(db: dict, username: str)->UserInDB:
    if username in db:
        user_in = db[username]
        return UserInDB(**user_in.dict())

def authenticate_user(auth_db: dict, username: str, password: str)->UserInDB | bool:
    user = get_user(auth_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None)->str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt