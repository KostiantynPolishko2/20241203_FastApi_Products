from fastapi import APIRouter, status, HTTPException, Path
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import joinedload
from schemas.product_schema import (ProductSchema, ProductSchemaPublic, ProductSchemaModify,
                     ProductSchemaCard, ProductSchemaProperty)
from schemas.property_schema import PropertySchemaInput
from schemas.response_schema import ResponseSchema
from typing import Annotated
from models.product import Product
from depends import db as db_service
import httpx

router = APIRouter(
    prefix='/product',
    tags=['Http request: Product'],
    responses={status.HTTP_400_BAD_REQUEST: {'description' : 'Bad Request'}}
)

model_params = Annotated[str, Path(description='weapons model', min_length=2)]

@router.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

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
async def add_new_product(request: ProductSchemaProperty, db:db_service)->ResponseSchema:

    product = Product(model=request.model.lower(), category=request.category.lower())

    db.add(product)
    db.commit()
    db.refresh(product)
    request_property = PropertySchemaInput.from_property(request.property, product.id)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url='http://127.0.0.3:8081/api/v1/weapons/property/',
                                         json=request_property.dict(), )
        return response.json()
    except ():
        db.delete(product)
        db.commit()
        return ResponseSchema(code=status.HTTP_400_BAD_REQUEST, status='not added', property=f'product {str(product.model).upper()}')

@router.put('/{model}', status_code=status.HTTP_202_ACCEPTED)
async def update_product(model: model_params, request: ProductSchema, db: db_service)->ResponseSchema:

    product = db.query(Product).filter(Product.model == model.lower()).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product \'{model.upper()}\' is absent in db!')

    db.query(Product).filter(Product.model == model).update(request.model_dump(exclude_unset=True))
    db.commit()

    return ResponseSchema(code=status.HTTP_202_ACCEPTED, status='updated', property=f'product {str(product.model).upper()}')

@router.delete('/{model}', status_code=status.HTTP_202_ACCEPTED)
async def delete_product(model: model_params, db: db_service)->ResponseSchema:

    product = db.query(Product).filter(Product.model == model.lower()).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product \'{model.upper()}\' is absent in db!')

    db.delete(product)
    db.commit()

    return ResponseSchema(code=status.HTTP_202_ACCEPTED, status='deleted', property=f'product {str(product.model).upper()}')

@router.patch('/{model}', status_code=status.HTTP_202_ACCEPTED)
async def modify_product(model: model_params, request: ProductSchemaModify, db: db_service)->ResponseSchema:

    product = db.query(Product).filter(Product.model == model.lower()).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'product \'{model.upper()}\' is absent in db!')

    request_update = request.model_dump(exclude_unset=True)
    for key, value in request_update.items():
        setattr(product, key, value)
    db.commit()

    return ResponseSchema(code=status.HTTP_202_ACCEPTED, status='modified', property=f'product {str(product.model).upper()}')
