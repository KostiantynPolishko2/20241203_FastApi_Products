from fastapi import APIRouter, status, Depends
from fastapi.responses import RedirectResponse
from schemas.property_schema import PropertySchemaInput, PropertySchema
from schemas.response_schema import ResponseSchema
from schemas.property_schema_dto import PropertySchemaDto
from models.property import Property
from handlers.map_handler import MapHandler
from depends import get_property_service, id_params
from services.property_service import PropertyService
from schemas.enum_schema import EnumAvailable

router = APIRouter(
    prefix='/property',
    tags=['Http request: Property'],
    responses={status.HTTP_400_BAD_REQUEST: {'description' : 'Bad Request'}},
)

@router.get('/', response_class=RedirectResponse, include_in_schema=False)
def docs():
    return RedirectResponse(url='/docs')

@router.get('/all')
async def get_properties_all(is_available: EnumAvailable, service: PropertyService = Depends(get_property_service))->list[PropertySchemaDto]:
   return service.s_get_all_available(is_available.value)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_new_property(request: PropertySchemaInput, service: PropertyService = Depends(get_property_service))->ResponseSchema:

    _property = MapHandler.props_schema_in_to_props_model(request, Property)
    service.s_add_new_property(_property)

    return ResponseSchema(code=status.HTTP_201_CREATED, status='created', property=f'property price {_property.price}')

@router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def modify_property(id: id_params, request: PropertySchema, service: PropertyService = Depends(get_property_service))->ResponseSchema:

    service.s_modify_property(id, request)
    return ResponseSchema(code=status.HTTP_202_ACCEPTED, status='updated', property=f'property id {request.id}')