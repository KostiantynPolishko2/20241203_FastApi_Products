from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse, Response, PlainTextResponse
from fastapi.encoders import jsonable_encoder
from typing import Union
from fastapi.exceptions import RequestValidationError
from infrastructures.weapons_exception import WeaponsException404

async def validation_exception_handler(request: Request, exc: RequestValidationError)->Union[JSONResponse, Response]:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'request': request.method, 'detail': exc.errors(), 'body': exc.body}),
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    return PlainTextResponse(str(f'request {request.method} error {exc.detail}'), status_code=exc.status_code)

async def base_exception_handler(request: Request, exc: Exception):
    return PlainTextResponse(str(f'request {request.method} error {exc.__str__()}'), status_code=500)

async def weapons_exception_handler(request: Request, exc: WeaponsException404):
    return PlainTextResponse(str(f'request {request.method} error {exc.detail}'), status_code=exc.status_code)