from sqlalchemy import Column, Integer, BigInteger, String, sql, Date

from tgbot.models.gino_PostgreSQL import TimedBaseModel


class Birthday(TimedBaseModel):
    __tablename__ = 'birthdays'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger)
    name = Column(String(100), nullable=False)
    birthday = Column(Date, nullable=False)
    phone_number = Column(String(100), default="Нет номера")

    query: sql.Select


class User(TimedBaseModel):
    __tablename__ = 'users'
    telegram_id = Column(BigInteger, primary_key=True)
    full_name = Column(String(100))
    username = Column(String(100))

    query: sql.Select
