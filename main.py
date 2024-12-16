from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from redis import Redis, ConnectionPool

app = FastAPI()

pool = ConnectionPool(host='127.0.0.1', port=6379, db=0)
r = Redis(connection_pool=pool)


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
def read_root():
    return RedirectResponse(url='/docs')

@app.get("/items/{id}")
def read_item(id: int, q: str = None):

    cached_value = r.get(f'item_{id}')
    if not cached_value:
        r.set(f'item_{id}', q or 'No Query')
        cached_value = r.get(f'item_{id}')

    return {"item_id": id, "q": cached_value}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=8000)