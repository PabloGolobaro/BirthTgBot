from aiogram import Dispatcher
from aiogram.types import Message
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


def register_user(dp: Dispatcher):
    dp.register_message_handler(show_menu, commands=["start"], state="*")
