from sqlalchemy.orm.session import Session

from src.db.entity import UserEntity
from src.domain.bot.model import User as BotUser


def get_user_by_id(user: BotUser, db: Session) -> UserEntity | None:
    user = db.query(UserEntity).filter_by(id=user.id).first()
    return user


def create_user(user: BotUser, db: Session) -> None:
    row = UserEntity(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(row)
    db.commit()
