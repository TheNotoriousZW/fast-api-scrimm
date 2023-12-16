from sqlite3 import Timestamp
from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class CreatePost(PostBase):
    pass

class UserOut(BaseModel):
    
    id: int
    email: EmailStr
    created_at: datetime


    class Config:
        from_attributes = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    likes: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):

    email: EmailStr
    password: str


class UserLogin(BaseModel):
    password: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    dir: Annotated[int, range(0,2)]
    post_id: int
    