import uvicorn
from fastapi import FastAPI
from product_routers import router
from server import HandleServer

app = HandleServer(title='Weapons')
local_host = '127.0.0.3'
port = 8081

if __name__ == '__main__':
    uvicorn.run(app(router), host=local_host, port=port)