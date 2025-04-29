from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from src.configuration.database import get_db
from src.db.entity import UserEntity

from .model import User

router = APIRouter()


@router.get("")
async def get_user_list(db: Annotated[Session, Depends(get_db)]) -> List[User]:
    return db.query(UserEntity).all()  # type: ignore
