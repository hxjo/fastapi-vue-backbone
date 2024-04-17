from datetime import datetime
from typing import TYPE_CHECKING, Union

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.user.models import User


class AdminTokenBase(SQLModel):
    token: str
    expires_at: datetime
    user_id: int = Field(foreign_key="users.id")


class AdminToken(AdminTokenBase, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    expires_at: datetime = Field(index=True)
    user: "User" = Relationship(sa_relationship_kwargs={"lazy": "raise"})


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class NewPassword(BaseModel):
    token: str
    password: str

