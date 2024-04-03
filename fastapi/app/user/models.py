from typing import Union

from fastapi import UploadFile
from pydantic import EmailStr
from sqlalchemy import Column
from sqlmodel import AutoString, Field, SQLModel

from app.common.models import FileType


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)
    username: str


class User(UserBase, table=True):
    __tablename__ = "users"

    id: Union[int, None] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    avatar_url: Union[UploadFile, None] = Field(sa_column=Column(FileType()))


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    avatar_url: Union[UploadFile, None] = None


# Properties to receive via API on update, all are optional
class UserUpdate(SQLModel):
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    avatar_url: Union[UploadFile, None] = None


# Properties to return via API
class UserOut(UserBase):
    id: int
    is_active: bool
    avatar_url: Union[str, None] = None
