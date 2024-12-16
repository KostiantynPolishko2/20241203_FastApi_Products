import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from supplier_schema import SupplierSchema, SupplierSchemaInput, SupplierSchemaPublic
from contextlib import asynccontextmanager
from redis_config import redis_open, redis_close
from sqlalchemy.orm import Session
from typing import Annotated
from supplier_model import Supplier
from depends import get_db

async def delete_suppliers():
    all_pks = SupplierSchema.all_pks()
    [SupplierSchema.delete(pk) for pk in all_pks]

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_open(app)
    yield
    await delete_suppliers()
    redis_close(app)

app = FastAPI(lifespan=lifespan)


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def read_docs():
    return RedirectResponse(url='/docs')


@app.get('/suppliers')
async def read_suppliers()->list[SupplierSchemaPublic]:
    all_pks = SupplierSchema.all_pks()
    suppliers = [SupplierSchema.get(pk) for pk in all_pks]
    return suppliers


@app.post('/new-supplier', status_code=status.HTTP_201_CREATED)
async def add_new_supplier(request: SupplierSchemaInput, db: Annotated[Session, Depends(get_db)])->SupplierSchemaPublic:

    supplier = Supplier(name=request.name, budget=request.budget)
    try:
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'failed request to db!')


@app.get('/health')
async def health_check():
    return {"status": "healthy"}


if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=8000)