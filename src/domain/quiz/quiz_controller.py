from fastapi import APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.orm.session import Session

from src.configuration.database import get_db
from src.db.entity import QuizEntity

from .model import Quiz, QuizCreate, ResourceId

router = APIRouter(prefix="/v1/quiz")


@router.get("")
async def get_quiz_list(db: Session = Depends(get_db)) -> list[Quiz]:
    return db.query(QuizEntity).all()  # type: ignore


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_quiz(data: QuizCreate, db: Session = Depends(get_db)) -> ResourceId:
    row = QuizEntity(**data.model_dump())
    db.add(row)
    db.commit()
    return row


@router.get("/random")
async def get_quiz_randomly(db: Session = Depends(get_db)) -> Quiz:
    return db.query(QuizEntity).order_by(func.RAND()).first()
