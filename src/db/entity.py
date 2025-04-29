from sqlalchemy import BigInteger, Column, Integer, String

from src.configuration.database import Base


class UserEntity(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    score = Column(Integer, default=0)
