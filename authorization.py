import jwt
import os
import models, schemas
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from sqlalchemy.orm import Session


load_dotenv()


SECERET_KEY = os.getenv("SECERET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_access_token(token)

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expiry = datetime.utcnow() + expires_delta
    else:
        expiry = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expiry})
    encoded_jwt = jwt.encode(to_encode, SECERET_KEY, algorithm = ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt


def verify_access_token(token:str):
    try:
        payload = jwt.decode(token, SECERET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        print(user_id)
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
