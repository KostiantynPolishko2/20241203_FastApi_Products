import uvicorn
from src.app import server

local_host = '127.0.0.3'
port = 8081

if __name__ == '__main__':
    uvicorn.run(server, host=local_host, port=port)