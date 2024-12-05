from fastapi import APIRouter, status, HTTPException, Depends
from schemas import PropertySchemaInput, ProductSchemaResponse, PropertySchema
from models import Property
from database import db as db_service, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/property',
    tags=['Http request: Property'],
    responses={status.HTTP_400_BAD_REQUEST: {'description' : 'Bad Request'}}
)

@router.get('/')
async def property_home():
    return {'message': 'run controller products'}

def map_property_orm_schema_to_sql(_property: PropertySchemaInput, orm_model_class: type[Property])->Property:
    return orm_model_class(**_property.model_dump())

@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_new_property(request: PropertySchemaInput, db: Session=Depends(get_db))->ProductSchemaResponse:

    _property = map_property_orm_schema_to_sql(request, Property)

    db.add(_property)
    db.commit()

    return ProductSchemaResponse(code=status.HTTP_201_CREATED, status='created', property=f'property price {_property.price}')