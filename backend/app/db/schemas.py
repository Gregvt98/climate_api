from pydantic import BaseModel
import typing as t
from datetime import datetime
from typing import Set, Union, Dict

#schemas user
class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None

    class Config:
        orm_mode = True
        #arbitrary_types_allowed = True

class UserOut(UserBase):
    pass

class UserHashedPassword(UserBase):
    hashed_password: t.Optional[str] = None
    id: int

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
    image_url: t.Optional[str]
    longitude: float
    latitude: float
    created_at: datetime
    sentiment_analysis: SentimentAnalysisBase

class PostCreate(PostBase):
    latitude: float
    longitude: float
    title: str
    content: str
    user_id: int # User ID = 6 is anonymous

class EventBase(BaseModel):
    pass
    class Config:
        orm_mode = True
        #arbitrary_types_allowed = True

class EventCreate(EventBase):
    log_level: str
    ip_address: t.Optional[str]
    user_agent: t.Optional[str]
    event_type: str
    event_data: t.Optional[Dict]
    user_id:  t.Optional[int]

class EventEdit(EventBase):
    event_data: t.Optional[Dict]

class EventOut(EventBase):
    id: str
    timestamp: datetime
    event_type: str
    log_level: str

class CommentBase(BaseModel):
    content: str
    user_id: int

class CommentCreate(CommentBase):
    pass