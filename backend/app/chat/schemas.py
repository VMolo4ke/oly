from typing import Literal

from pydantic import BaseModel, Field


class ChatHistoryItem(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=20000)


class ChatClientMessage(BaseModel):
    """Сообщение клиента, пришедшее по WebSocket."""

    message: str = Field(min_length=1, max_length=4000)
    history: list[ChatHistoryItem] = Field(default_factory=list, max_length=40)

