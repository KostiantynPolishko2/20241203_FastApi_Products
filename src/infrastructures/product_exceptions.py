from fastapi import HTTPException, status

products_empty_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='table products is empty in db!'
)

products_not_added_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='product did not added to table product!'
)