import uvicorn
from app_auth.server import HandleServer
from app_auth.auth_routers import router

app = HandleServer(title='Authorization')
local_host = '127.0.0.3'
port = 8081

if __name__ == '__main__':
    uvicorn.run(app(router), host=local_host, port=port)