from fastapi import APIRouter, status, HTTPException, Depends
from schemas import PropertySchema, ProductSchemaResponse
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

@router.post('/', status_code=status.HTTP_201_CREATED, deprecated=True)
async def add_new_property(request: PropertySchema, db: Session=Depends(get_db))->ProductSchemaResponse:

    _property = Property(price=request.price, is_available=request.is_available, description=request.description)
    db.add(_property)
    db.commit()

    return ProductSchemaResponse(code=status.HTTP_201_CREATED, status='created', property=f'property price {_property.price}')