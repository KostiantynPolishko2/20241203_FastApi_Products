from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from models import UserModel
from infrastructures import none_user_exceptions

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, username: str)->UserModel:
        user: UserModel = self.db.query(UserModel).filter(UserModel.username == username.lower()).first()
        if not user:
            raise none_user_exceptions
        return user

    def is_exist_user(self):
        pass

    def add_user_to_db(self):
        pass