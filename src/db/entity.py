from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from src.configuration.database import Base


class BaseMixin:
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.utc_timestamp(),
        onupdate=func.utc_timestamp(),
    )


class UserEntity(BaseMixin, Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    score = Column(Integer, default=0)
    quiz_id = Column(Integer, ForeignKey("quiz.id"), nullable=True)

    quiz = relationship("QuizEntity", back_populates="current_users", uselist=False)


class QuizEntity(BaseMixin, Base):
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    answer = Column(Integer, nullable=False)

    current_users = relationship("UserEntity", back_populates="quiz")
