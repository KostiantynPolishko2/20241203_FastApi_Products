from fastapi import HTTPException, status

property_exc_404 = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='table properties is empty in db!'
)

property_exc_400 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='property did not added to table properties!'
)