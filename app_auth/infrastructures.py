from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

auth_exceptions = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

create_user_exceptions = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User with this email already exist"
)

none_user_exceptions = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User with this nane did not found"
)

add_user_exceptions = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="failed to add new username to db"
)