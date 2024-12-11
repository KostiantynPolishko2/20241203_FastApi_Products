import uvicorn
from routing.product_routers import router as product_router
from routing.property_routers import router as property_router
from src.server import HandleServer

app = HandleServer(title='Weapons')
local_host = '127.0.0.3'
port = 8081

if __name__ == '__main__':
    uvicorn.run(app(product_router, property_router), host=local_host, port=port)