import bcrypt
import os


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITM")
TOKEN_EXPIRE_MINUTES = os.getenv("TOKEN_EXPIRE_MINUTES")

def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt)
    return hashed.decode("utf-8")

def vefify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("uft-8"), hashed_password.encode("utf-8"))