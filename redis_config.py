# from redis_om import get_redis_connection
#
# redis = get_redis_connection(host="127.0.0.1", port=6379, decode_responses=True)

from fastapi import FastAPI
from redis_om import Migrator
from redis import Redis, ConnectionPool

def redis_open(app: FastAPI)->None:
    pool = ConnectionPool(host='127.0.0.1', port=6379, db=0)
    app.state.redis = Redis(connection_pool=pool)
    Migrator().run()

def redis_close(app: FastAPI)->None:
    app.state.redis.close()