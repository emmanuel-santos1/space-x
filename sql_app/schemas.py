from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    name: str
    last_name: str
    password: str


class User(UserBase):
    id: int
    name: str
    last_name: str

    class Config:
        orm_mode = True


class Task(BaseModel):
    id: int
    type: str
    title: Optional[str] = ""
    description: Optional[str] = ""
    category: Optional[str] = ""


class Label(BaseModel):
    id = int
    trello_id = str
    name = str
