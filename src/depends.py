from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from databases.database import SessionLocal

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db = Annotated[Session, Depends(get_db)]