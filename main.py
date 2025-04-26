from fastapi import FastAPI

from src.db import entity
from src.domain.router import router

app = FastAPI()
app.include_router(router=router)


@app.on_event("startup")
def on_startup():
    from src.configuration.database import engine

    entity.Base.metadata.create_all(bind=engine)
