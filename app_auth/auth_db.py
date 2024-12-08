from schemas import UserInDB
from uuid import UUID

auth_db = {
    'johndoe' : UserInDB(
        username='johndoe',
        email='johndoe@example.com',
        disabled=False,
        id=UUID('12345678-1234-1234-1234-123456789abc'),
        hashed_password='fake_hashed_secret'
    ),
    'alice': UserInDB(
        username='alice',
        email='alice@example.com',
        disabled=True,
        id=UUID('12345678-1234-1234-1234-123456789bcd'),
        hashed_password='fake_hashed_secret2'
    )
}
