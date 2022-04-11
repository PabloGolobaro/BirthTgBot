from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.utils.markdown import hbold

from tgbot.keyboards.inline_main_menu import main_menu
# from tgbot.models import quik_commands as command
# from tgbot.models.schemas.user import Birthday
from tgbot.models import django_commands as command
from birthdays.models import User, Birthday



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

async def info_month(id,bot: Bot):
    birthdays = await command.select_all_birthdays(id)
    text = "В этом месяце день рождения:\n---------------\n"
    for birthday in birthdays:
        date_string = birthday.birthday
        date_time_object = datetime.fromisoformat(str(date_string))
        a = date_time_object.month
        c = date_time_object.day
        b = datetime.today().date().month
        d = datetime.today().date().day
        if a == b:
            age = datetime.today() - date_time_object
            age = int(age.days / 365)
            format_data = "%d/%m/%y"
            text += f"{birthday.name} - {hbold(date_time_object.date())}\nему исполнится {age}\n---------------\n"
    if text != "В этом месяце день рождения:\n---------------\n":
        await bot.send_message(id, text, reply_markup=main_menu)
        print(text)
    else:
        await bot.send_message(id, "Ничего!", reply_markup=main_menu)
        print("Ничего!")


async def info_week(id,bot: Bot):
    birthdays = await command.select_all_birthdays(id)
    text = "На неделю вперед дни рождения:\n---------------\n"
    for i in range(1, 8):
        DAY = datetime.today().date() + timedelta(i)
        for birthday in birthdays:
            date_string = birthday.birthday
            date_time_object = datetime.fromisoformat(str(date_string))
            a = date_time_object.month
            c = date_time_object.day
            b = DAY.month
            d = DAY.day
            if a == b and c == d:
                age = datetime.today() - date_time_object
                age = int(age.days / 365)
                text += f"{birthday.name} - {hbold(date_time_object.date())}\nему исполнится {age}\n---------------\n"
    if text != "На неделю вперед дни рождения:\n---------------\n":
        await bot.send_message(id, text, reply_markup=main_menu)
        print(text)
    else:
        await bot.send_message(id, "Ничего!", reply_markup=main_menu)
        print("Ничего!")
