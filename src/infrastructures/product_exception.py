from fastapi import HTTPException, status

products_empty = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='table products is empty in db!'
)