import models
import schemas
import bcrypt

from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.SignUp).filter(models.SignUp.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()



def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def hash_password(plain_text: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_text.encode('utf-8'), salt)
    return hashed_password


def check_password(plain_text, hashed_password):
    return bcrypt.checkpw(plain_text.encode('utf-8'), hashed_password)


def create_user(db: Session, user: schemas.SignUp):
    hashed_password = hash_password(user.password)
    db_user = models.SignUp(email = user.email, password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user    


def login(db: Session, user: schemas.SignUp):
    db_user = db.query(models.SignUp).filter(models.SignUp.email == user.email).first()
    if not db_user:
        return "User does not exist, please login!"
    print(f"=== {db_user.password} ====")
    verify_passcode = check_password(user.password, db_user.password)
    print(verify_passcode)

    if verify_passcode:
        return "Welcome Sir, you are logged In."
    return "Wrong Creds!"    