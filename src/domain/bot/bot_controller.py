from devtools import debug
from fastapi import APIRouter, Body, Request
from pydantic import HttpUrl

from src.configuration.config import settings
from src.core.telegram import Telegram

from .model import Update

router = APIRouter(prefix="/v1")
telegram = Telegram(settings.TELEGRAM_BOT_TOKEN)


@router.post("/")
async def webhook(request: Request):
    r = await request.json()
    r = Update.parse_obj(r)
    debug(r)
    return "OK"


@router.get("/me")
async def get_me():
    return await telegram.get_bot_info()


@router.get("/wb")
async def get_webhook():
    return await telegram.get_webhook()


@router.post("/wb")
async def set_webhook(url: HttpUrl = Body(..., embed=True)):
    return await telegram.set_webhook(url)
