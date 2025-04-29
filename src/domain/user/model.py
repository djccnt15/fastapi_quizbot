from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    score: int | None = None
