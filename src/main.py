from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import entity
from src.domain.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.configuration.database import engine

    entity.Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["OPTIONS", "GET", "POST"],
    allow_headers=["*"],
)
