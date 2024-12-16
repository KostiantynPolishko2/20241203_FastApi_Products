docker build --tag fastapi-demo-redis:v1.0.0 .

docker run --detach --publish 8000:8000 --name fastapi-cache_v1 fastapi-demo-redis:v1.0.0