from typing import Literal

from pydantic import BaseModel


class Message(BaseModel):
    content: str
    timestamp: float
    type: Literal["error", "default"] = "default"


class MessageOut(BaseModel):
    message: Message
