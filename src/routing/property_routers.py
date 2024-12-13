from fastapi import APIRouter, status, Depends, Path
from fastapi.responses import RedirectResponse
from schemas.property_schema import PropertySchemaInput, PropertySchema
from schemas.response_schema import ResponseSchema
from models.property import Property
from depends import get_property_service
from services.property_service import PropertyService
from typing import Annotated

router = APIRouter(
    prefix='/property',
    tags=['Http request: Property'],
    responses={status.HTTP_400_BAD_REQUEST: {'description' : 'Bad Request'}},
)

id_params = Annotated[int, Path(description='id of weapons property', gt=0)]

def map_property_orm_schema_to_sql(_property: PropertySchemaInput, orm_model_class: type[Property])->Property:
    return orm_model_class(**_property.model_dump())

@router.get('/', response_class=RedirectResponse, include_in_schema=False)
def docs():
    return RedirectResponse(url='/docs')

@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_new_property(request: PropertySchemaInput, service: PropertyService = Depends(get_property_service))->ResponseSchema:

    _property = map_property_orm_schema_to_sql(request, Property)
    service.s_add_new_property(_property)

    return ResponseSchema(code=status.HTTP_201_CREATED, status='created', property=f'property price {_property.price}')

@router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def modify_property(id: id_params, request: PropertySchema, service: PropertyService = Depends(get_property_service))->ResponseSchema:

    service.s_modify_property(id, request)
    return ResponseSchema(code=status.HTTP_202_ACCEPTED, status='updated', property=f'property id {request.id}')