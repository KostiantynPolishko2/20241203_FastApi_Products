from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.sql.annotation import Annotated

from schemas.property_schema import PropertySchemaInput, PropertySchema
from schemas.response_schema import ResponseSchema
from models.property import Property
from depends import get_db, get_property_service
from sqlalchemy.orm import Session
from services.property_service import PropertyService

router = APIRouter(
    prefix='/property',
    tags=['Http request: Property'],
    responses={status.HTTP_400_BAD_REQUEST: {'description' : 'Bad Request'}},
)

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

# @router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED)
# async def modify_property(id: int, request: PropertySchema, db: Session=Depends(get_db))->ResponseSchema:
#
#     _property = db.query(Property).filter(Property.id == id).first()
#     if not _property:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'property id \'{id}\' is absent in db!')
#
#     request_update = request.model_dump(exclude_unset=True)
#     for key, value in request_update.items():
#         setattr(_property, key, value)
#     db.commit()
#
#     return ResponseSchema(code=status.HTTP_202_ACCEPTED, status='updated', property=f'property id {_property.id}')