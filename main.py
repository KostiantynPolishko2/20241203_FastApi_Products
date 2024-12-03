import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Product, Base
from schemas import ProductSchema, ProductSchemaPublic
from typing import Union, List, Optional, Annotated
from responces import ProductSchemaResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get('/', deprecated=True)
async def home():
    return {'message' : 'run app products'}

@app.get('/products', status_code=status.HTTP_200_OK)
async def get_products_all(db: Session = Depends(get_db))->list[ProductSchemaPublic]:
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'table products is empty in db!')

    return list[ProductSchemaPublic](products)

@app.get('/product/{model}', status_code=status.HTTP_200_OK)
async def get_product_by_name(model: str, db: Session = Depends(get_db))->ProductSchemaPublic:
    product = db.query(Product).filter(Product.model == model).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product \'{model}\' is absent in db!')

    return product

@app.post('/product', status_code=status.HTTP_201_CREATED)
async def add_new_product(request: ProductSchema, db: Session = Depends(get_db))->ProductSchemaResponse:
    product = Product(model=request.model.lower(), category=request.category.lower())
    try:
        db.add(product)
        db.commit()
        return ProductSchemaResponse(code=status.HTTP_201_CREATED, status='created', property=f'product {str(product.model).upper()}')
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'failed request to db!')

if __name__ == '__main__':
    uvicorn.run(app)