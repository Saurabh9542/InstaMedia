import models
import schemas
import bcrypt
from fastapi import HTTPException, security, Depends
from sqlalchemy.orm import Session
from database import verify_access_token

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session):
    return db.query(models.User).all()


def get_posts_by_user(db: Session, user_id: int):
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User does not exist with id-{user_id}")
    
    db_posts = db.query(models.Post).filter(models.Post.owner_id == user_id).all()
    
    return db_posts



def get_posts(db: Session):
    return db.query(models.Post).all()


def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def hash_password(plain_text: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_text.encode('utf-8'), salt)
    return hashed_password


def check_password(plain_text, hashed_password):
    return bcrypt.checkpw(plain_text.encode('utf-8'), hashed_password)


def create_user(db: Session, user: schemas.User):
    hashed_password = hash_password(user.password)
    db_user = models.User(email = user.email, password = hashed_password, user_name = user.user_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user    


def login(db: Session, user: schemas.User):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        return "User does not exist, please login!"
    verify_passcode = check_password(user.password, db_user.password)

    if verify_passcode:
        return db_user
    return "Wrong Creds!"    



