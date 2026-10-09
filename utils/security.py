import bcrypt
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "10080"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: dict) -> str:
    data_copy = data.copy()
    expity_date = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    data_copy.update({"exp": expity_date})
# Fixed
    token = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
# Fixed
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = data.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not Validate Credentials.")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not Validate Credentials.")

