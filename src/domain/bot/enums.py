from enum import StrEnum


class ChatTypeEnum(StrEnum):
    private = "private"
    group = "group"
    supergroup = "supergroup"
    channel = "channel"
