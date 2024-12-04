from fastapi import status, HTTPException
from models import Product, Base
from sqlalchemy.ext.declarative import declarative_base

class ProductRepository:

    def __init__(self, db:declarative_base):
        self.db=db

    def get_all(self):
        products = self.db.query(Product).all()
        if not products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'table products is empty in db!')

        return products
