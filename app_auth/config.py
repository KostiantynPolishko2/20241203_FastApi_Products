import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ['JWT_SECRET_KEY']
ALGORITHM = os.environ['JWT_ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ['JWT_ACCESS_TOKEN_EXPIRE_MINUTES'])