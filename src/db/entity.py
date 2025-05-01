from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.configuration.database import Base


class BaseMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.utc_timestamp(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.utc_timestamp(),
        onupdate=func.utc_timestamp(),
    )


class UserEntity(BaseMixin, Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str | None] = mapped_column(String(100))
    first_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    score: Mapped[int] = mapped_column(Integer, default=0)
    quiz_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("quiz.id"))

    quiz = relationship("QuizEntity", back_populates="current_users", uselist=False)


class QuizEntity(BaseMixin, Base):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Integer)

    current_users = relationship("UserEntity", back_populates="quiz")
