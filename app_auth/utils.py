from schemas import User

def fake_decode_token(token):
    return User(
        username=token + "fake_decoded", email="john@example.com", full_name="John Doe"
    )