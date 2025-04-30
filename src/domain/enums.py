from enum import StrEnum, auto


class DomainEnum(StrEnum):
    BOT = auto()
    USER = auto()


class ResponseEnum(StrEnum):
    OK = "OK"
