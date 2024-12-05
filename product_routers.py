from fastapi import APIRouter, status, HTTPException, Path, Depends
from sqlalchemy.orm import joinedload

from schemas import (ProductSchema, ProductSchemaPublic, ProductSchemaResponse, ProductSchemaModify,
                     ProductSchemaCard, ProductSchemaProperty)
from typing import Annotated
from models import Product, Property
from database import db as db_service
# from product_repository import ProductRepository

router = APIRouter(
    prefix='/product',
    tags=['Http request: Product'],
    responses={status.HTTP_400_BAD_REQUEST: {'description' : 'Bad Request'}}
)

model_params = Annotated[str, Path(description='weapons model', min_length=2)]

# def find_product_by_name(model: str, db: SessionLocal):
#     product = db.query(Product).filter(Product.model == model).first()
#     if not product:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product \'{model.upper()}\' is absent in db!')

@router.get('/', deprecated=True)
async def product_home():
    return {'message' : 'run controller products'}

@router.get('/all')
async def get_products_all(db:db_service)->list[ProductSchemaPublic]:
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'table products is empty in db!')

    return list[ProductSchemaPublic](products)

@router.get('/{model}', status_code=status.HTTP_200_OK)
async def get_product_card_by_name(model: model_params, db:db_service)->ProductSchemaCard:

    product = db.query(Product).options(joinedload(Product.property)).filter(Product.model == model.lower()).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product \'{model.upper()}\' is absent in db!')

    return ProductSchemaCard.from_property(model=product.model, _property=product.property)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_new_product(request: ProductSchema, db:db_service)->ProductSchemaResponse:
    product = Product(model=request.model.lower(), category=request.category.lower())
    try:
        db.add(product)
        db.commit()
        return ProductSchemaResponse(code=status.HTTP_201_CREATED, status='created', property=f'product {str(product.model).upper()}')
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'failed request to db!')

@router.put('/{model}', status_code=status.HTTP_202_ACCEPTED)
async def update_product(model: model_params, request: ProductSchema, db: db_service)->ProductSchemaResponse:

    product = db.query(Product).filter(Product.model == model.lower()).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product \'{model.upper()}\' is absent in db!')

    db.query(Product).filter(Product.model == model).update(request.model_dump(exclude_unset=True))
    db.commit()

    return ProductSchemaResponse(code=status.HTTP_202_ACCEPTED, status='updated', property=f'product {str(product.model).upper()}')

@router.delete('/{model}', status_code=status.HTTP_202_ACCEPTED)
async def delete_product(model: model_params, db: db_service)->ProductSchemaResponse:

    product = db.query(Product).filter(Product.model == model.lower()).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product \'{model.upper()}\' is absent in db!')

    db.delete(product)
    db.commit()

    return ProductSchemaResponse(code=status.HTTP_202_ACCEPTED, status='deleted', property=f'product {str(product.model).upper()}')

@router.patch('/{model}', status_code=status.HTTP_202_ACCEPTED)
async def modify_product(model: model_params, request: ProductSchemaModify, db: db_service)->ProductSchemaResponse:

    product = db.query(Product).filter(Product.model == model.lower()).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product \'{model.upper()}\' is absent in db!')

    request_update = request.model_dump(exclude_unset=True)
    for key, value in request_update.items():
        setattr(product, key, value)
    db.commit()

    return ProductSchemaResponse(code=status.HTTP_202_ACCEPTED, status='modified', property=f'product {str(product.model).upper()}')

# def get_product_repository()->ProductRepository:
#     return ProductRepository(db_service)
#
# @router.get('/products-db', status_code=status.HTTP_200_OK)
# async def get_products_all_db(product_repository: Annotated[ProductRepository, Depends(get_product_repository)]):
#     return product_repository.get_all()
