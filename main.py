import models
import schemas
import crud
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal, engine, create_access_token, verify_access_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_access_token(token)

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.get("/users/", response_model=list[schemas.SignUp])
def read_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    users = crud.get_users(db)
    return users


@app.get("/users/{email}", response_model=schemas.SignUp)
def read_user(email: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_user = crud.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
def create_item_for_user(
    user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return crud.create_user_post(db=db, post=post, user_id=user_id)


@app.get("/users/{user_id}/posts", response_model = list[schemas.Post])
def get_posts_by_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    get_posts = crud.get_posts_by_user(db, user_id)
    print(get_posts)
    if get_posts:
        return get_posts
    
    raise HTTPException(status_code=200, detail=f"Nothing is posted by the user with id-{user_id}")



@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    items = crud.get_posts(db)
    return items


@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup_user(req: schemas.SignUp, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email = req.email)
    print(db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    return crud.create_user(db, req)


@app.post("/login")
def login_user(req: schemas.SignUp, db: Session = Depends(get_db)):
    check_creds = crud.login(db, req)
    print(check_creds.id)

    if not check_creds:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    access_token = create_access_token(data = {"sub": str(check_creds.id)})
    return {"access_token": access_token, "token_type": "bearer"}


