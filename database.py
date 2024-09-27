import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


try:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./testDB.db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

    print("DB connected Success")
except Exception as e:
    print("DB not connected", e)



SECERET_KEY = "qwertyuiopasdfghjklzxcvbnm"
ALGORITHM = "HS256"

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

        

# if __name__ == "__main__":
    # data = {'user_id': '123', 'username': 'saurabh'}
    # create_access_token(data)

    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzIiwidXNlcm5hbWUiOiJzYXVyYWJoIiwiZXhwIjoxNzI3NDQ1NjM2fQ.GaA2kUc2M4SkGVr2d7v_zPmAT8PIxTvpfmNbkcy5DDk"
    # verify_access_token(token)
    