from schemas import UserInDB
from uuid import UUID

auth_db = {
    'johndoe' : UserInDB(
        username='johndoe',
        email='johndoe@example.com',
        is_disabled=False,
        guid=UUID('12345678-1234-1234-1234-123456789abc'),
        hashed_password='fake_hashed_secret'
    ),
    'alice': UserInDB(
        username='alice',
        email='alice@example.com',
        is_disabled=True,
        guid=UUID('12345678-1234-1234-1234-123456789bcd'),
        hashed_password='fake_hashed_secret2'
    )
}
