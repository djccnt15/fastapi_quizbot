from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request
from pydantic import HttpUrl
from sqlalchemy.orm.session import Session

from src.configuration.config import settings
from src.configuration.database import get_db
from src.core.telegram import Telegram
from src.domain.enums import ResponseEnum
from src.domain.quiz import quiz_service
from src.domain.user import user_service

from .model import Update

router = APIRouter(prefix="/v1/bot")
telegram = Telegram(settings.TELEGRAM_BOT_TOKEN)


@router.post(f"/{settings.TELEGRAM_BOT_TOKEN.get_secret_value()}")
async def webhook(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> ResponseEnum:
    req = await request.json()
    update = Update.model_validate(req)
    message = update.message
    assert message
    user = message.from_
    assert user
    db_user = user_service.get_user_by_id(user=user, db=db)
    if not db_user:
        user_service.create_user(user=user, db=db)
    assert db_user

    text = message.text
    assert text
    msg = "✨ '문제' 또는 '퀴즈'라고 말씀하시면 문제를 냅니다!"
    if "문제" in text or "퀴즈" in text:
        quiz = quiz_service.get_rand_quiz(db=db)
        db_user.quiz_id = quiz.id
        msg = f"{quiz.question}\n\n{quiz.content}"
    elif db_user.quiz_id and text.isnumeric():
        correct = db_user.quiz.answer == int(text)
        msg = f"아쉽네요, {db_user.quiz.answer}번이 정답입니다."

        if correct:
            db_user.score += 1
            msg = f"{db_user.quiz.answer}번, 정답입니다!"

        db_user.quiz_id = None

    await telegram.send_message(message.chat.id, msg)
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
