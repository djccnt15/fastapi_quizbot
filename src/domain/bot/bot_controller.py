from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request
from pydantic import HttpUrl
from sqlalchemy.orm.session import Session

from src.configuration.config import settings
from src.configuration.database import get_db
from src.core.telegram import Telegram
from src.db.entity import UserEntity
from src.domain.enums import ResponseEnum

from .model import Update

router = APIRouter(prefix="/v1")
telegram = Telegram(settings.TELEGRAM_BOT_TOKEN)


@router.post(f"/{settings.TELEGRAM_BOT_TOKEN.get_secret_value()}")
async def webhook(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> ResponseEnum:
    req = await request.json()
    update = Update.model_validate(req)
    assert update.message
    user = update.message.from_
    assert user
    db_user = db.query(UserEntity).filter_by(id=user.id).first()

    if not db_user:
        row = UserEntity(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        db.add(row)
        db.commit()
    return ResponseEnum.OK


@router.get("/me")
async def get_me():
    return await telegram.get_bot_info()


@router.get("/wb")
async def get_webhook():
    return await telegram.get_webhook()


@router.post("/wb")
async def set_webhook(url: HttpUrl = Body(..., embed=True)):
    return await telegram.set_webhook(url)
