from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/health")
async def health():
    return 1


@router.get(path="/", response_class=RedirectResponse)
async def index_redirect():  # temporal index page redirect to swagger
    return "/docs"
