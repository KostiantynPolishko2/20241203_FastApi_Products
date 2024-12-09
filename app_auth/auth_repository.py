from sqlalchemy.orm import Session
from models import UserModel
from schemas import UserAuth
from infrastructures import none_user_exceptions, create_user_exceptions
from uuid import uuid4
from utils import get_password_hash

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, username: str)->UserModel:
        user: UserModel = self.db.query(UserModel).filter(UserModel.username == username.lower()).first()
        if not user:
            raise none_user_exceptions
        return user

    def is_exist_user(self, username: str)->None:
        user: UserModel = self.db.query(UserModel).filter(UserModel.username == username.lower()).first()
        if user is not None:
            raise create_user_exceptions

    def add_user_to_db(self, request: UserAuth)->int:
        new_user = UserModel(
            username=request.username,
            email=request.email,
            is_disabled=request.is_disabled,
            guid=uuid4(),
            hashed_password=get_password_hash(request.password)
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user.id