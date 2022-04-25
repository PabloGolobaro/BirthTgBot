from aiogram import Dispatcher
import asyncpg
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.types.message import ContentType
from aiogram import types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot import host
from tgbot.keyboards.inline_main_menu import Base_file, main_menu
from tgbot.misc.states import Base_load
from pathlib import Path
import pandas as pd
from datetime import datetime
from tgbot.models import django_commands as command
# from tgbot.models.schemas.user import User, Birthday
from birthdays.models import Birthday
from django.contrib.auth.models import User
from tgbot.handlers.Notificatio_func import notification_scheduler, info_week, info_month


async def update_db(path, id):
    try:
        await command.delete_all_birthdays(id)
        birthdays = pd.read_excel(path)
        for row in birthdays.itertuples(index=False):
            name = row[0]
            Date = row[1]
            phone = row[2]
            if isinstance(phone, float):
                phone = None
            date_year = Date.date()
            await command.add_birthday(id, name, date_year, phone)
        print(birthdays.head())
        users = await command.select_all_birthdays(id)
        print(f"После добавления: {users=}")
    except Exception as err:
        print(err)


async def show_menu(message: Message):
    log_text = ""
    # host = socket.gethostbyname(socket.gethostname())
    try:
        user = await command.select_user(telegram_id=message.from_user.id)
    except:
        password = User.objects.make_random_password(length=8)
        user: User = await command.add_user(
            password=password,
            full_name=message.from_user.full_name,
            telegram_id=message.from_user.id,
            username=message.from_user.username
        )
        log_text = f"Похоже вы здесь впервые.\n{hbold('Ваши данные для входа на сайт:')}\nИмя пользователя: {user.username}\nПароль: {password}\nНе потеряйте их!\n"
    text = f"Здравствуй {hbold(message.from_user.full_name)}\n{log_text}Переход на сайт по адресу: {host}:8000\nВыберите необходимый пункт меню"
    await message.answer(text, reply_markup=main_menu)


async def full_base(call: CallbackQuery):
    full_base = await command.select_all_birthdays(call.from_user.id)

    string = "№ | Имя | Дата Рождения | Телефон|\n"
    for birthday in full_base:
        string += "№"
        birthday: Birthday
        string += str(birthday.name) + " |"
        string += str(birthday.birthday) + " |"
        string += str(birthday.phone_number) + " |"
        string += "\n"
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(string, reply_markup=main_menu)


async def send_base(call: CallbackQuery):
    await call.message.edit_reply_markup(Base_file)


async def menu(call: CallbackQuery):
    await call.message.edit_reply_markup(main_menu)


async def send_base_file(call: CallbackQuery):
    await Base_load.Load_state.set()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Отправьте файл БД в формате Excel.")


async def download_document(message: types.Message, state: FSMContext, scheduler: AsyncIOScheduler):
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
        scheduler.add_job(notification_scheduler, "cron", hour="8,20", args=(message.from_user.id, message.bot,),
                          start_date=datetime.now(), id=user_id)
    else:
        # scheduler.add_job(notification_scheduler, "cron", hour="8,20", minute=5, args=(message.from_user.id,),
        #                   start_date=datetime.now(), id=user_id)
        scheduler.add_job(notification_scheduler, "cron", hour="8,20", args=(message.from_user.id, message.bot,),
                          start_date=datetime.now(), id=user_id)


async def download_error(message: types.Message):
    await message.answer("Ошибка получения файла БД.", reply_markup=Base_file)


async def send_month(call: CallbackQuery):
    await info_month(call.from_user.id, call.message.bot)
    await call.message.edit_reply_markup(reply_markup=None)


async def send_week(call: CallbackQuery):
    await info_week(call.from_user.id, call.message.bot)
    await call.message.edit_reply_markup(reply_markup=None)


def register_user(dp: Dispatcher):
    dp.register_message_handler(show_menu, commands=["start"], state="*")
    dp.register_callback_query_handler(full_base, text="full_base", state="*")

    dp.register_callback_query_handler(send_base, text="users_base", state="*")
    dp.register_callback_query_handler(menu, text="menu", state="*")
    dp.register_callback_query_handler(send_base_file, text="send_base_file", state="*")
    dp.register_callback_query_handler(send_month, text="month", state="*")
    dp.register_callback_query_handler(send_week, text="week", state="*")
    dp.register_message_handler(download_document, content_types=ContentType.DOCUMENT, state=Base_load.Load_state)
    dp.register_message_handler(download_error, content_types=ContentType.ANY, state=Base_load.Load_state)
