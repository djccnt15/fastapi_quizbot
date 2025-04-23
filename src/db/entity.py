from sqlalchemy import Column, Integer, String

from src.configuration.database import Base


class UserEntity(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
