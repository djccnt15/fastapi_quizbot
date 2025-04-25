from fastapi import FastAPI

from src.domain.router import router

app = FastAPI()
app.include_router(router=router)
