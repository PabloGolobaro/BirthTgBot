import datetime

from asyncpg import UniqueViolationError

from tgbot.models.schemas.user import Birthday, User


async def add_user(telegram_id: int, full_name: str, username: str = None):
    try:
        user = User(telegram_id=telegram_id, full_name=full_name, username=username)

        await user.create()
    except UniqueViolationError:
        pass
    return user


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def add_birthday(telegram_id: int, name: str, birthday: datetime.date, phone_number: str = None):
    try:
        birthday = Birthday(telegram_id=telegram_id, name=name, birthday=birthday, phone_number=phone_number)

        await birthday.create()
    except UniqueViolationError:
        pass
    return birthday


async def select_all_birthdays(telegram_id: int):
    users = await Birthday.query.where(Birthday.telegram_id == telegram_id).gino.all()
    return users


async def delete_all_birthdays(telegram_id: int):
    await Birthday.delete.where(Birthday.telegram_id == telegram_id).gino.status()

# async def select_user(id: int):
#     user = await User.query.where(User.id == id).gino.first()
#     return user


# async def count_users():
#     total = await db.func.count(User.id).gino.scalar()
#     return total


# async def update_user_email(id: int, email):
#     user = await User.get(id)
#     await user.update(email=email).apply()
