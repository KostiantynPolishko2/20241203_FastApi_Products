from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=RedirectResponse, include_in_schema=False)
def read_root():
    return RedirectResponse(url='/docs')

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=8000)