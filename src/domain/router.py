from fastapi import APIRouter

from .bot import bot_controller
from .default import router as default_router
from .enums import DomainEnum

router = APIRouter(prefix="/api")

router.include_router(router=default_router)
router.include_router(
    router=bot_controller.router,
    tags=[DomainEnum.BOT],
)
