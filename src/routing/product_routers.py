from fastapi import APIRouter, Path
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from schemas.product_schema import (ProductSchemaPublic,
                     ProductSchemaCard, ProductSchemaProperty)
from schemas.property_schema import PropertySchemaInput
from schemas.response_schema import ResponseSchema
from typing import Annotated
from depends import get_product_service
import httpx

from repositories.weapons_repository import *

from services.product_service import ProductService


router = APIRouter(
    prefix='/product',
    tags=['Http request: Product'],
    responses={status.HTTP_400_BAD_REQUEST: {'description' : 'Bad Request'}}
)

model_params = Annotated[str, Path(description='weapons model', min_length=2)]
product_service = Annotated[ProductService, Depends(get_product_service)]


@router.get('/', response_class=RedirectResponse, include_in_schema=False)
def docs():
    return RedirectResponse(url='/docs')

@router.get('/all')
def get_products_all(service: product_service)->list[ProductSchemaPublic]:
    return service.get_all()

@router.get('/{model}', status_code=status.HTTP_200_OK)
def get_product_card_by_name(model: model_params, service: product_service)->ProductSchemaCard:
    product = service.get_product_card_by_name(model)
    return ProductSchemaCard.from_property(model=product.model, _property=product.property)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_new_product(request: ProductSchemaProperty, service: product_service)->ResponseSchema:

    product = Product(model=request.model.lower(), category=request.category.lower())
    product_id = service.add_new_product(product)
    request_property = PropertySchemaInput.from_property(request.property, product_id)

    async with httpx.AsyncClient() as client:
        response = await client.post(url='http://127.0.0.3:8081/api/v1/weapons/property/',json=request_property.dict())

        if response.status_code >= 400:
            service.delete_product(product)
            return ResponseSchema(code=status.HTTP_400_BAD_REQUEST, status='not added', property=f'product {str(product.model).upper()}')

    return ResponseSchema(code=status.HTTP_201_CREATED, status='created', property=f'product {str(product.model).upper()}')

@router.put('/{model}', status_code=status.HTTP_202_ACCEPTED)
async def update_product(model: model_params, request: ProductSchema, service: product_service)->ResponseSchema:

    service.update_product(model, request)
    return ResponseSchema(code=status.HTTP_202_ACCEPTED, status='updated', property=f'product {str(request.model).upper()}')

@router.delete('/{model}', status_code=status.HTTP_202_ACCEPTED)
async def delete_product(model: model_params, service: product_service)->ResponseSchema:

    service.delete_product_by_name(model)
    return ResponseSchema(code=status.HTTP_202_ACCEPTED, status='deleted', property=f'product {str(model).upper()}')

@router.patch('/{model}', status_code=status.HTTP_202_ACCEPTED)
async def modify_product(model: model_params, request: ProductSchemaModify, service: product_service)->ResponseSchema:
    service.modify_product(model, request)
    return ResponseSchema(code=status.HTTP_202_ACCEPTED, status='modified', property=f'product {str(model).upper()}')
