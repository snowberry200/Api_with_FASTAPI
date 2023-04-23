from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


# USER
class CreateUser(BaseModel):
    email: EmailStr
    password: str


class RespondUser(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# POST


class PostBase(BaseModel):
    title: str
    comment: str
    published: bool = True


class CreatePost(PostBase):
    pass


class RespondPost(PostBase):
    id: int
    owner_id: int
    owner: RespondUser

    class Config:
        orm_mode = True


class PostVotes(PostBase):
    updates: RespondPost
    votes: int

    class Config:
        orm_mode = True

# LOGIN


class RespondLogin(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token = str
    token_type = str


class RespondToken(Token):
    pass


class TokenData(BaseModel):
    id: Optional[str] = None


# VOTE
class Vote(BaseModel):
    update_id: int
    dir: conint(le=1)
