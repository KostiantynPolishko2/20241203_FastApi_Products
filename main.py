from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import uvicorn
from supplier_schema import SupplierSchema, SupplierSchemaResponse
from redis_om import Migrator
from redis import Redis, ConnectionPool

app = FastAPI()

pool = ConnectionPool(host='127.0.0.1', port=6379, db=0)
redis = Redis(connection_pool=pool)
Migrator().run()

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def read_docs():
    return RedirectResponse(url='/docs')

@app.get('/suppliers')
async def read_suppliers()->list[SupplierSchemaResponse]:
    all_pks = SupplierSchema.all_pks()
    suppliers = [SupplierSchema.get(pk) for pk in all_pks]
    return suppliers

@app.get('/supplier/search/')
async def read_supplier_by_name(name: str)->SupplierSchemaResponse:
    # suppliers = SupplierSchema.find(SupplierSchema.name==name).all()
    all_pks = SupplierSchema.all_pks()

    suppliers = [SupplierSchema.get(pk) for pk in all_pks]
    if not suppliers:
        raise HTTPException(status_code=404, detail="Supplier not found")

    match_supplier = [supplier for supplier in suppliers if supplier.name.lower()==name.lower()][0]
    if not match_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return match_supplier

@app.post('/new-supplier')
async def add_new_supplier(name: str, budget: float):
    supplier = SupplierSchema(name=name, budget=budget)
    supplier.save()

    return supplier.key().title()

@app.delete('/suppliers')
async def delete_suppliers()->str:
    all_pks = SupplierSchema.all_pks()
    [SupplierSchema.delete(pk) for pk in all_pks]

    return 'suppliers deleted'

@app.get('/health')
async def health_check():
    return {"status": "healthy"}

if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=8000)