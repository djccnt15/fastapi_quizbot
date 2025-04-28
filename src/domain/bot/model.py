from datetime import datetime

from pydantic import BaseModel, Field

from .enums import ChatTypeEnum


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str


class Chat(BaseModel):
    id: int
    type: ChatTypeEnum
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None


class Message(BaseModel):
    message_id: int
    from_: User | None = Field(
        None,
        title="Sender",
        description="Sender, empty for messages sent to channels",
        alias="from",
    )
    chat: Chat
    date: datetime
    text: str | None = Field(None, max_length=4096)


class Update(BaseModel):
    update_id: int
    message: Message | None = None
