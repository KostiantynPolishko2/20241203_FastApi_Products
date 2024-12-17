from fastapi import FastAPI
from redis_om import Migrator
from redis import Redis, ConnectionPool
from supplier_schema import SupplierSchema, SupplierSchemaPublic
from sqlalchemy.orm import Session
import json
from supplier_model import Supplier

def redis_open(app: FastAPI)->None:
    pool = ConnectionPool(host='127.0.0.1', port=6379, db=0)
    app.state.redis = Redis(connection_pool=pool, decode_responses=True)
    Migrator().run()


def redis_close(app: FastAPI)->None:
    app.state.redis.flushdb()
    app.state.redis.close()


async def delete_suppliers():
    all_pks = SupplierSchema.all_pks()
    [SupplierSchema.delete(pk) for pk in all_pks]


def load_suppliers(app: FastAPI, db: Session)->None:
    suppliers_sql = db.query(Supplier).all()
    suppliers_pyd = [SupplierSchemaPublic.model_validate(supplier_sql).model_dump() for supplier_sql in suppliers_sql]
    app.state.redis.set('suppliers', json.dumps(suppliers_pyd))
