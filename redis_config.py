from fastapi import FastAPI
from redis_om import Migrator
from redis import Redis, ConnectionPool
from supplier_schema import SupplierSchema, SupplierSchemaPublic
from sqlalchemy.orm import Session
from supplier_model import Supplier
import json


def redis_open(app: FastAPI)->None:
    pool = ConnectionPool(host='127.0.0.1', port=6379, db=0)
    app.state.redis = Redis(connection_pool=pool, decode_responses=True)
    Migrator().run()

    # data = get_all_suppliers_from_db(db)
    # app.state.redis.set('suppliers', json.dumps(data))


def redis_close(app: FastAPI)->None:
    app.state.redis.flushdb()
    app.state.redis.close()


async def delete_suppliers():
    all_pks = SupplierSchema.all_pks()
    [SupplierSchema.delete(pk) for pk in all_pks]


def get_all_suppliers_from_db(db: Session)->list[type[SupplierSchemaPublic]]:
    try:
        data = db.query(Supplier).all()
        return data
    except:
        return []
