from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from schemas import ProductSchemaPublic
from models import Product, Base

class ProductRepository:
    db: Session

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        products = self.db.query(Product).all()
        if not products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'table products is empty in db!')

        return products
