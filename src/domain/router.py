from fastapi import APIRouter

from .bot import bot_controller
from .default import default_controller
from .enums import DomainEnum

API_PREFIX = "/api"

router = APIRouter()

router.include_router(router=default_controller.router)
router.include_router(
    prefix=API_PREFIX,
    router=bot_controller.router,
    tags=[DomainEnum.BOT],
)
