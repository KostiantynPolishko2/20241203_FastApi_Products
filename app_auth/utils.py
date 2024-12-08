from schemas import User, UserInDB

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token)->User:
    return User(
        username=token + "fake_decoded",
        email="john@example.com",
        full_name="John Doe"
    )

def fake_hash_password(password: str):
    return "fake_hashed_" + password