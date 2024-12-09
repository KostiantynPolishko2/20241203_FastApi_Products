import uuid

from sqlalchemy import Column, Integer, String, Boolean, Uuid
from database import Base, engine
from sqlalchemy.dialects.postgresql import UUID

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    is_disabled = Column(Boolean, name='disable')
    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)