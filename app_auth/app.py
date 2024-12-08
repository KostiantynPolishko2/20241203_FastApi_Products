from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from typing import Annotated
from deps import get_current_user
from schemas import User

app = FastAPI()

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

@app.get('items')
async def read_items(current_user: Annotated[User, Depends(get_current_user)])->User:
    return current_user