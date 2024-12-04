from fastapi import APIRouter, status, HTTPException
from schemas import PropertySchema
from models import Property

router = APIRouter(
    prefix='/property',
    tags=['Http request: Property'],
    responses={status.HTTP_400_BAD_REQUEST: {'description' : 'Bad Request'}}
)

@router.get('/')
async def property_home():
    return {'message': 'run controller products'}