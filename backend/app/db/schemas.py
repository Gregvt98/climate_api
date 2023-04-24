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

class PostBase(BaseModel):
    pass

class PostOut(PostBase):
    pass
    #created_at: datetime
    #updated_at: datetime


class PostCreate(PostBase):
    title: t.Optional[str] = None
    content: t.Optional[str] = None
    user_id: t.Optional[int] = None

    class Config:
        orm_mode = True


class PostEdit(PostBase):
    content: t.Optional[str] = None

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    title: str
    content: str
    user_id: t.Optional[int]

    class Config:
        orm_mode = True