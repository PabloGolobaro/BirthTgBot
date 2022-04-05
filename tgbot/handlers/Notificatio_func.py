from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.utils.markdown import hbold
from tgbot.models import quik_commands as command
from tgbot.models.schemas.user import Birthday


async def notification_scheduler(user_id, bot: Bot):
    birthdays = await command.select_all_birthdays(user_id)
    text = ""
    # /---------------------------------------------------------------
    for birthday in birthdays:
        birthday: Birthday
        date_string = birthday.birthday
        date_time_object = datetime.fromisoformat(str(date_string))
        a = date_time_object.month
        b = datetime.today().date().month
        c = date_time_object.day
        d = datetime.today().date().day
        if a == b and c == d:
            age = datetime.today() - date_time_object
            age = int(age.days / 365)
            if birthday.phone_number != None:
                phone = birthday.phone_number
            else:
                phone = "Не указан!"
            text += f"Сегодня день рождения у {hbold(birthday.name)}\nЕму сегодня исполнилось {age}\nНомер телефона: {phone}\n----------------\n"
    # /------------------------------------------------
    DAY = datetime.today().date() + timedelta(1)
    for birthday in birthdays:
        birthday: Birthday
        date_string = birthday.birthday
        date_time_object = datetime.fromisoformat(str(date_string))
        a = date_time_object.month
        b = DAY.month
        c = date_time_object.day
        d = DAY.day
        if a == b and c == d:
            age = datetime.today() - date_time_object
            age = int(age.days / 365)
            if birthday.phone_number != None:
                phone = birthday.phone_number
            else:
                phone = "Не указан!"
            text += f"Завтра день рождения у {hbold(birthday.name)}\nЕму исполнится {age}\nНомер телефона: {phone}\n----------------\n"
    # /------------------------------------------------------------

    if text != "":
        await bot.send_message(user_id, text)
        print(text)
