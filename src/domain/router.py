from fastapi import APIRouter

from .default import router as default_router

router = APIRouter(prefix="/api")

router.include_router(router=default_router)
