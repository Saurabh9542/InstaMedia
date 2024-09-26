from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    description: str
    photo: str | None = None


class PostCreate(PostBase):
    pass

class SignUp(BaseModel):
    email: EmailStr
    password: str
    user_name: str



class Post(PostBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Post] = []

    class Config:
        orm_mode = True