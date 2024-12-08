from app_auth.app import app as app_auth
import uvicorn

local_host = '127.0.0.3'
port = 8081

if __name__ == '__main__':
    uvicorn.run(app_auth, host=local_host, port=port)