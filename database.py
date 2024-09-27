import os
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

try:
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

    print("DB connected Success")
except Exception as e:
    print("DB not connected", e)





def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



        

# if __name__ == "__main__":
    # data = {'user_id': '123', 'username': 'saurabh'}
    # create_access_token(data)

    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzIiwidXNlcm5hbWUiOiJzYXVyYWJoIiwiZXhwIjoxNzI3NDQ1NjM2fQ.GaA2kUc2M4SkGVr2d7v_zPmAT8PIxTvpfmNbkcy5DDk"
    # verify_access_token(token)
    