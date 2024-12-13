from src.config import HandleServer
from handlers.exception_handler import *
from routing.product_router import router as product_router
from routing.property_router import router as property_router

handleServer = HandleServer(title='Weapons')
server = handleServer()

server.include_router(product_router)
server.include_router(property_router)

server.add_exception_handler(RequestValidationError, validation_exception_handler)
server.add_exception_handler(HTTPException, http_exception_handler)
server.add_exception_handler(Exception, base_exception_handler)
server.add_exception_handler(WeaponsException404, weapons_exception_handler)