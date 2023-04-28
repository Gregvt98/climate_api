from pydantic import BaseModel
import typing as t

#schemas user
class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"


#schemas post

class SentimentAnalysisBase(BaseModel):
    type: str
    score: float
    ratio: float

    class Config:
        orm_mode = True

class SentimentAnalysisCreate(SentimentAnalysisBase):
    type: str
    score: float
    ratio: float


class SentimentAnalysisOut(SentimentAnalysisBase):
    id: int

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    pass

class PostEdit(PostBase):
    title: t.Optional[str] = None
    content: t.Optional[str] = None

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    title: str
    content: t.Optional[str] = None
    user_id: t.Optional[int]
    #sentiment_analysis: t.Optional[SentimentAnalysisBase]

    class Config:
        orm_mode = True

class PostOut(PostBase):
   pass
    #created_at: datetime
    #updated_at: datetime


class PostCreate(PostBase):
    latitude: float
    longitude: float
    title: t.Optional[str] = None
    content: t.Optional[str] = None
    user_id: t.Optional[int] = None

    class Config:
        orm_mode = True
