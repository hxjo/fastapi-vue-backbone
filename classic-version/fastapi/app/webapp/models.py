from typing import Union, Literal

from pydantic import BaseModel
from app.user.models import UserOut

class Message(BaseModel):
    content: str
    timestamp: float
    type: Literal['error', 'default'] = "default"

class MessageOut(BaseModel):
    message: Message

class HomeOut(BaseModel):
    user: Union[UserOut, None]


class AppOut(BaseModel):
    user: UserOut
    message: Union[Message, None] = None