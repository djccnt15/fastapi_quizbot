from sqlalchemy import func
from sqlalchemy.orm.session import Session

from src.db.entity import QuizEntity


def get_rand_quiz(db: Session) -> QuizEntity:
    quiz = db.query(QuizEntity).order_by(func.RAND()).first()
    return quiz
