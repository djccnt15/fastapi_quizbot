from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import entity
from src.domain.router import router

app = FastAPI()
app.include_router(router=router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["OPTIONS", "GET", "POST"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    from src.configuration.database import engine

    entity.Base.metadata.create_all(bind=engine)
