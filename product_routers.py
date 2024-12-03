from fastapi import APIRouter, status, Depends, HTTPException
from schemas import ProductSchema, ProductSchemaPublic
from typing import Union, List, Optional, Annotated
from responces import ProductSchemaResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from database import engine
from models import Product, Base

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix='/weapons',
    tags=['Http request: Product'],
    responses={status.HTTP_400_BAD_REQUEST: {'description' : 'Bad Request'}}
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

db_service = Annotated[Session, Depends(get_db)]

@router.get('/', deprecated=True)
async def home():
    return {'message' : 'run app products'}

@router.get('/products', status_code=status.HTTP_200_OK)
async def get_products_all(db: db_service)->list[ProductSchemaPublic]:
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'table products is empty in db!')

    return list[ProductSchemaPublic](products)

@router.get('/product/{model}', status_code=status.HTTP_200_OK)
async def get_product_by_name(model: str, db: db_service)->ProductSchemaPublic:
    product = db.query(Product).filter(Product.model == model).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product \'{model}\' is absent in db!')

    return product

@router.post('/product', status_code=status.HTTP_201_CREATED)
async def add_new_product(request: ProductSchema, db: db_service)->ProductSchemaResponse:
    product = Product(model=request.model.lower(), category=request.category.lower())
    try:
        db.add(product)
        db.commit()
        return ProductSchemaResponse(code=status.HTTP_201_CREATED, status='created', property=f'product {str(product.model).upper()}')
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'failed request to db!')