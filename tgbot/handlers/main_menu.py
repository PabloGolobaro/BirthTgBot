import asyncio

import asyncpg
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters import CommandStart
from aiogram import types
from tgbot.keyboards.inline_main_menu import Base_file, main_menu
# from loader import dp, db, bot, scheduler
from tgbot.misc.states import Base_load
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from tgbot.models import quik_commands as command
from tgbot.models.schemas.user import User


async def update_db(path, id):
    # создаем БД
    # try:
    #     db.create_table_users(id)
    # except Exception as err:
    #     print(err)
    #     db.delete_users(id)
    try:
        birthdays = pd.read_excel(path)
        for row in birthdays.itertuples(index=False):
            name = row[0]
            Date = row[1]
            phone = row[2]
            date_year = Date.date()
            await command.add_birthday(id, name, date_year, phone)
        print(birthdays.head())
        users = command.select_all_birthdays(id)
        print(f"После добавления: {users=}")
    except Exception as err:
        print(err)

    # print(db.select_all_users())


# async def notification(id):
#     while (True):
#         users = db.select_all_users(id)
#         text = ""
#         # /---------------------------------------------------------------
#         for user in users:
#             date_string = user[2]
#             date_time_object = datetime.fromisoformat(date_string)
#             a = date_time_object.month
#             b = datetime.today().date().month
#             c = date_time_object.day
#             d = datetime.today().date().day
#             if a == b and c == d:
#                 age = datetime.today() - date_time_object
#                 age = int(age.days / 365)
#                 if user[3] != None:
#                     phone = user[3]
#                 else:
#                     phone = "Не указан!"
#                 text += f"Сегодня день рождения у {hbold(user[1])}\nЕму сегодня исполнилось {age}\nНомер телефона: {phone}\n----------------\n"
#         # /------------------------------------------------
#         DAY = datetime.today().date() + timedelta(1)
#         for user in users:
#             date_string = user[2]
#             date_time_object = datetime.fromisoformat(date_string)
#             a = date_time_object.month
#             b = DAY.month
#             c = date_time_object.day
#             d = DAY.day
#             if a == b and c == d:
#                 age = datetime.today() - date_time_object
#                 age = int(age.days / 365)
#                 if user[3] != None:
#                     phone = user[3]
#                 else:
#                     phone = "Не указан!"
#                 text += f"Завтра день рождения у {hbold(user[1])}\nЕму исполнится {age}\nНомер телефона: {phone}\n----------------\n"
#         # /------------------------------------------------------------
#
#         if text != "":
#             await bot.send_message(id, text)
#             print(text)
#         await asyncio.sleep(60 * 60 * 24)
#

async def notification_scheduler(user_id):
    users = db.select_all_users(user_id)
    text = ""
    # /---------------------------------------------------------------
    for user in users:
        date_string = user[2]
        date_time_object = datetime.fromisoformat(date_string)
        a = date_time_object.month
        b = datetime.today().date().month
        c = date_time_object.day
        d = datetime.today().date().day
        if a == b and c == d:
            age = datetime.today() - date_time_object
            age = int(age.days / 365)
            if user[3] != None:
                phone = user[3]
            else:
                phone = "Не указан!"
            text += f"Сегодня день рождения у {hbold(user[1])}\nЕму сегодня исполнилось {age}\nНомер телефона: {phone}\n----------------\n"
    # /------------------------------------------------
    DAY = datetime.today().date() + timedelta(1)
    for user in users:
        date_string = user[2]
        date_time_object = datetime.fromisoformat(date_string)
        a = date_time_object.month
        b = DAY.month
        c = date_time_object.day
        d = DAY.day
        if a == b and c == d:
            age = datetime.today() - date_time_object
            age = int(age.days / 365)
            if user[3] != None:
                phone = user[3]
            else:
                phone = "Не указан!"
            text += f"Завтра день рождения у {hbold(user[1])}\nЕму исполнится {age}\nНомер телефона: {phone}\n----------------\n"
    # /------------------------------------------------------------

    if text != "":
        await bot.send_message(user_id, text)
        print(text)


async def info_month(id):
    users = db.select_all_users(id)
    text = "В этом месяце день рождения:\n---------------\n"
    for user in users:
        date_string = user[2]
        date_time_object = datetime.fromisoformat(date_string)
        a = date_time_object.month
        c = date_time_object.day
        b = datetime.today().date().month
        d = datetime.today().date().day
        if a == b:
            age = datetime.today() - date_time_object
            age = int(age.days / 365)
            format_data = "%d/%m/%y"
            text += f"{user[1]} - {hbold(date_time_object.date())}\nему исполнится {age}\n---------------\n"
    if text != "В этом месяце день рождения:\n---------------\n":
        await bot.send_message(id, text, reply_markup=main_menu)
        print(text)
    else:
        await bot.send_message(id, "Ничего!", reply_markup=main_menu)
        print("Ничего!")


async def info_week(id):
    users = db.select_all_users(id)
    text = "На неделю вперед дни рождения:\n---------------\n"
    for i in range(1, 8):
        DAY = datetime.today().date() + timedelta(i)
        for user in users:
            date_string = user[2]
            date_time_object = datetime.fromisoformat(date_string)
            a = date_time_object.month
            c = date_time_object.day
            b = DAY.month
            d = DAY.day
            if a == b and c == d:
                age = datetime.today() - date_time_object
                age = int(age.days / 365)
                text += f"{user[1]} - {hbold(date_time_object.date())}\nему исполнится {age}\n---------------\n"
    if text != "На неделю вперед дни рождения:\n---------------\n":
        await bot.send_message(id, text, reply_markup=main_menu)
        print(text)
    else:
        await bot.send_message(id, "Ничего!", reply_markup=main_menu)
        print("Ничего!")


@dp.message_handler(CommandStart)
async def show_menu(message: Message):
    text = f"Здравствуй {hbold(message.from_user.full_name)}\nВыберите необходимый пункт меню"
    await message.answer(text, reply_markup=main_menu)
    try:
        user: User = await command.add_user(
            name=message.from_user.full_name,
            id=message.from_user.id
        )
        print(f"User added {user}")
    except asyncpg.exceptions.UniqueViolationError:
        user = await command.select_user(id=message.from_user.id)
        print(f"User is already exusts {user}")


@dp.callback_query_handler(text="full_base")
async def send_base(call: CallbackQuery):
    full_base = command.select_all_birthdays(call.from_user.id)
    string = "№ | Имя | Дата Рождения | Телефон|\n"
    for record in full_base:
        string += "№"
        for element in record:
            string += str(element) + " |"
        string += "\n"
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(string, reply_markup=main_menu)


@dp.callback_query_handler(text="users_base")
async def send_base(call: CallbackQuery):
    await call.message.edit_reply_markup(Base_file)


@dp.callback_query_handler(text="menu")
async def send_base(call: CallbackQuery):
    await call.message.edit_reply_markup(main_menu)


@dp.callback_query_handler(text="month")
async def send_month(call: CallbackQuery):
    await info_month(call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=None)


@dp.callback_query_handler(text="week")
async def send_week(call: CallbackQuery):
    await info_week(call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=None)


@dp.callback_query_handler(text="send_base_file")
async def send_base(call: CallbackQuery):
    await Base_load.Load_state.set()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Отправьте файл БД в формате Excel.")


@dp.message_handler(content_types=ContentType.DOCUMENT, state=Base_load.Load_state)
async def download_document(message: types.Message, state: FSMContext):
    path_to_download = Path().joinpath("Users", f"{message.from_user.id}")
    path_to_download.mkdir(parents=True, exist_ok=True)
    path_to_download = path_to_download.joinpath("Base.xlsx")
    await message.document.download(destination=path_to_download)
    await update_db(path_to_download, message.from_user.id)
    await state.finish()
    await message.answer("Файл базы данных обновлен.\n Включен режи оповещения", reply_markup=main_menu)
    # scheduler.ctx.add_instance(message.from_user.id, declared_class=str)
    user_id = str(message.from_user.id)
    if scheduler.get_job(job_id=user_id):
        scheduler.remove_job(job_id=user_id)
        scheduler.add_job(notification_scheduler, "cron", hour="8,20", minute=5, args=(message.from_user.id,),
                          start_date=datetime.now(), id=user_id)
    else:
        scheduler.add_job(notification_scheduler, "cron", hour="8,20", minute=5, args=(message.from_user.id,),
                          start_date=datetime.now(), id=user_id)
    # Создаем напоминатель в потоке loop
    # dp.loop.create_task(notification(message.from_user.id))


@dp.message_handler(content_types=ContentType.ANY, state=Base_load.Load_state)
async def download_error(message: types.Message):
    await message.answer("Ошибка получения файла БД.", reply_markup=Base_file)
