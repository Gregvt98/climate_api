from pydantic import BaseModel
import typing as t
from datetime import datetime
from typing import Set, Union

#schemas user
class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None

    class Config:
        orm_mode = True

class UserOut(UserBase):
    pass

class UserCreate(UserBase):
    password: str

class UserEdit(UserBase):
    password: t.Optional[str] = None

class User(UserBase):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"
class SentimentAnalysisBase(BaseModel):
    type: t.Optional[str]
    score: t.Optional[float]
    ratio: t.Optional[float]

    class Config:
        orm_mode = True

class SentimentAnalysisOut(SentimentAnalysisBase):
    id: int

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

    class Config:
        orm_mode = True

class PostEdit(PostBase):
    title: t.Optional[str] = None
    content: t.Optional[str] = None

class Post(PostBase):
    pass

class PostOut(PostBase):
    id: int
    title: str
    content: t.Optional[str] = None
    user_id: t.Optional[int]
    user: UserOut
    image_url: str
    longitude: float
    latitude: float
    created_at: datetime
    #sentiment_analysis: Union[SentimentAnalysisBase, None]

class PostCreate(PostBase):
    latitude: float
    longitude: float
    title: str
    content: str
    user_id: t.Optional[int] = 0 # User ID = 0 is default (=anonymous)
